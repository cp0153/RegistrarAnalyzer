#!/usr/bin/python3

import dryscrape
from bs4 import BeautifulSoup
import time
import json
import os
import sys
from registrarparse import *
from terminfo import *
from cmdmanage import *
from django.db.utils import IntegrityError

# Import settings for django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "se_site.settings.prd")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "se_site.settings.dev")
import django

django.setup()
from registrar_analyzer.models import Courses

# Parse and check command line arguments
if len(sys.argv) != 5:
    print("\nUsage:\n\tpython3 scrapeterms.py <start_semester> <end_semester> <course> <out_file>")
    print('Example:\n\tpython3 scrapeterms.py "Fall 2005" "Spring 2008" cp1 ./results/cp1.txt\n')
    print(sys.argv)
    exit()

startSemester = sys.argv[1]
endSemester = sys.argv[2]
courseInput = sys.argv[3]
outFilePath = sys.argv[4]
if startSemester not in termDict:
    print("\nThe start semester must be between Fall 2000 and Spring 2017.\n")
    exit()
if endSemester not in termDict:
    print("\nThe end semester must be between Fall 2000 and Spring 2017.\n")
    exit()
if courseInput not in courseDict:
    print("\nYou did not enter a valid Computer Science course.")
    print("Choose from any of the following:")
    print("\tcp1, cp2, cp3, cp4, assembly, opl, foundations, "
          "arch,\n\tos, algorithms, ai, compiler, cg2, cg1, "
          "cv, cybercrime,\n\tdc1, dc2, datamining, db1, db2, "
          "gui1, gui2,\n\tml, mobileapp2, mobilerobotics1, "
          "mobilerobotics2,\n\tnlp, selected, se1, se2, special\n")
    exit()

# Get the indices for the semester numbers
startTermNum = termDict[startSemester]
startTermIndex = allSemesters.index(startTermNum)
endTermNum = termDict[endSemester]
endTermIndex = allSemesters.index(endTermNum)

# Check that the start semester isn't greater than the end semester
if int(startTermNum) > int(endTermNum):
    print("\nThe end semester cannot be less than the start semester.\n")
    exit()

# Create the Registrar Parser Object to store the data
dryscrape.start_xvfb()  # This line might not be needed
parser = RegistrarParser(startSemester, endSemester,
                         courseInput, outFilePath)
print(parser)

# Open the file
with open(outFilePath, 'w') as outFile:
    logf = open("dberrors.log", "+w")
    # Tell the user which course they're scraping and which semesters
    readableCourse = parser.getReadableCourseName()
    scrapePrompt = "\n> You chose to scrape the course " + readableCourse
    print(scrapePrompt)
    parser.writeStringToFile(outFile, scrapePrompt + "\n")

    scrapePrompt = "> You chose to scrape semesters "
    scrapePrompt += startSemester + " through " + endSemester
    print(scrapePrompt)
    parser.writeStringToFile(outFile, scrapePrompt + "\n")

    # Set up necessary variables for scraping
    beginning = time.time()
    currentSemIndex = startTermIndex  # Start counter for semester scraping
    courseUrl = parser.getCourseUrl()  # Formatted course string for registrar

    # Keeping track of time will also be important for analytics.
    timeSoFar = 0
    timeLeft = 0
    semsParsed = 0

    # This while loop goes through the range of semesters specified
    # Every iteration here represents one semester
    while currentSemIndex <= endTermIndex:

        # Get start time for this semester
        currSemTimeStart = time.time()

        # Form the URL.
        currentTermNum = allSemesters[currentSemIndex]
        scrapeUrl = parser.createRegistrarUrl(currentTermNum, courseUrl)

        scrapePrompt = "\n>>> Getting Info for Semester " + numDict[currentTermNum]
        print(scrapePrompt)
        parser.writeStringToFile(outFile, scrapePrompt + "\n")

        # Now that we have the user input, request the URL.
        responseSoup = parser.getSiteBody(scrapeUrl, 5)
        semProfs = {}  # Professor section count for this semester
        sections = []  # The list of course sections for this semester
        courseGroupDivs = parser.getCourseGroupDivs(responseSoup)
        for courseGroupDiv in courseGroupDivs:

            # With the group we can get individual sections.
            scrapePrompt = "\n>> Reached a group result."
            parser.writeStringToFile(outFile, scrapePrompt + "\n")
            courseSections = parser.getCourseSectionDivs(courseGroupDiv)
            i = 1  # Debugging Course Section Counter
            multSecCnt = 0 # Counter to find out how many sections had multiple meeting info
            for courseSection in courseSections:

                # Check first for a cancelled section.
                scrapePrompt = "\n>> Parsing Course Section " + str(i)
                parser.writeStringToFile(outFile, scrapePrompt + "\n")
                if parser.isCancelled(courseSection) is True:
                    scrapePrompt = "> This course section is cancelled."
                    parser.writeStringToFile(outFile, scrapePrompt + "\n")
                    i += 1
                else:

                    # We need the section details div before proceeding.
                    sectionDetailsDiv = parser.getDetailsDiv(courseSection)
                    meetInfoDicts = []

                    # From the section details, find quick info first
                    try:
                        quickDict = parser.getQuickInfoDetails(sectionDetailsDiv)
                        parser.writeQuickInfoToFile(outFile, quickDict)
                    except:
                        scrapePrompt = "> Something went wrong trying to get quick info for this section."
                        print(scrapePrompt)
                        parser.writeStringToFile(outFile, scrapePrompt + "\n")

                    # From section details, search for meeting info
                    try:
                        meetingInfoDivs = parser.getMeetingInfoDivs(sectionDetailsDiv)
                        if meetingInfoDivs is None:
                            parser.writeStringToFile(outFile, "> This course section has no meeting information.\n")
                        else:
                            for sectionMeetingDiv in meetingInfoDivs:
                                meetList = parser.getSectionMeetingInfo(sectionMeetingDiv, semProfs, i)
                                meetDict = meetList[0]
                                meetInfoDicts.append(meetDict)
                                semProfs = meetList[1]
                                parser.writeMeetingInfoToFile(outFile, meetDict)
                    except:
                        scrapePrompt = "> Something went wrong trying to get meeting info for this section."
                        print(scrapePrompt)
                        parser.writeStringToFile(outFile, scrapePrompt + "\n")
                    i += 1

                    # Now that we've parsed this course section, combine the
                    # info into one dictionary.
                    sectionDict = parser.combineInfoDicts(quickDict,
                                                          meetInfoDicts,
                                                          numDict[currentTermNum],
                                                          readableCourse)
                    sections.append(sectionDict)

                    # After getting the section dictionary, use it to enter a DB entry.
                    for meeting in meetInfoDicts:
                        try:
                            if meetInfoDicts.index(meeting) == 0:
                                course = Courses(course_name=readableCourse,
                                                 semester=sectionDict['semester'],
                                                 time_start=meeting['timeStart'],
                                                 time_end=meeting['timeEnd'],
                                                 enroll_now=sectionDict['enrollNow'],
                                                 enroll_max=sectionDict['enrollMax'],
                                                 honors=sectionDict['honors'],
                                                 credit_value=int(sectionDict['creditValue'][0]),
                                                 meeting_days=meeting['days'],
                                                 instructor=meeting['instructor'],
                                                 room=meeting['room']
                                                 )
                            else:
                                multSecCnt += 1
                                course = Courses(course_name=readableCourse,
                                                 semester=sectionDict['semester'],
                                                 time_start=meeting['timeStart'],
                                                 time_end=meeting['timeEnd'],
                                                 enroll_now="0", # Prevent duplicate enrollment
                                                 enroll_max=sectionDict['enrollMax'],
                                                 honors=sectionDict['honors'],
                                                 credit_value=int(sectionDict['creditValue'][0]),
                                                 meeting_days=meeting['days'],
                                                 instructor=meeting['instructor'],
                                                 room=meeting['room']
                                                 )
                            course.save()
                        except IntegrityError as e:
                            logf.write("Failed to download {0}: {1}\n".format(str(sectionDict), str(e)))
                        except:

                            # This means there were no meetings. Try saving the entry
                            # With a workaround
                            try:
                                course = Courses(course_name=readableCourse,
                                                 semester=sectionDict['semester'],
                                                 time_start=meetDict['timeStart'],
                                                 time_end=['timeEnd'],
                                                 enroll_now=sectionDict['enrollNow'],
                                                 enroll_max=sectionDict['enrollMax'],
                                                 honors=sectionDict['honors'],
                                                 credit_value=int(sectionDict['creditValue'][0]),
                                                 meeting_days="None",
                                                 instructor="None",
                                                 room="None"
                                                 )
                                course.save()
                            except:
                                logf.write("Failed to download {0}: {1}\n".format(str(sectionDict), str(e)))


        # Now add this semester's prof information to the semesterProfs list
        semesterProfsToAdd = []
        semesterProfsToAdd.append(numDict[currentTermNum])
        semesterProfsToAdd.append(semProfs)
        parser.addSemesterProfs(semesterProfsToAdd)

        # Also add the list of individual sections from this semester
        # possible spot to write to db?
        parser.addSectionListing(sections)
        try:
            print("> " + str(multSecCnt) + " sections had multiple meeting times.")
        except:
            pass

        # Get end time for this semester, and calculate time analytics.
        currSemTimeEnd = time.time()
        semParseTime = currSemTimeEnd - currSemTimeStart
        semsLeft = endTermIndex - currentSemIndex
        if semsLeft != 0:
            # Time Info Header for this section
            scrapePrompt = "\n>> Time Info:"
            print(scrapePrompt)
            parser.writeStringToFile(outFile, scrapePrompt + "\n")

            # Calculate time analytics
            timeSoFar += semParseTime
            semsParsed += 1
            timeAvg = timeSoFar / semsParsed
            timeLeft = timeAvg * semsLeft

            # Output the time analytics
            scrapePrompt = "> This semester took " + str(round(semParseTime, 3)) + " seconds"
            print(scrapePrompt)
            parser.writeStringToFile(outFile, scrapePrompt + "\n")

            scrapePrompt = "> " + str(semsParsed) + " Semesters Parsed in "
            scrapePrompt += str(round(timeSoFar, 3)) + " seconds."
            print(scrapePrompt)
            parser.writeStringToFile(outFile, scrapePrompt + "\n")

            scrapePrompt = "> " + str(semsLeft) + " Semesters Left, should take around "
            scrapePrompt += str(round(timeLeft, 3)) + " seconds."
            print(scrapePrompt)
            parser.writeStringToFile(outFile, scrapePrompt + "\n")

        # Move on to the next semester.
        currentSemIndex += 1

    # We've parsed all semesters, write out the data in the semesters
    scrapePrompt = "\n>>> Now writing out " + startSemester + " through "
    scrapePrompt += endSemester + " for " + readableCourse
    print(scrapePrompt)
    parser.writeStringToFile(outFile, scrapePrompt + "\n")
    parser.writeSemCountsToFile(outFile)

    # Now write out the professor total individual section counts
    scrapePrompt = "\n>>> Writing Professor Totals for " + readableCourse
    scrapePrompt += " for semesters " + startSemester + " through " + endSemester
    print(scrapePrompt)
    parser.writeStringToFile(outFile, scrapePrompt + "\n")
    parser.calculateProfTotals()
    parser.writeProfTotals(outFile)

    # Print how long this took.
    finished = time.time()
    runningTime = round(finished - beginning, 3)

    scrapePrompt = "\n>>> All of this took " + str(runningTime) + " seconds."
    print(scrapePrompt)
    parser.writeStringToFile(outFile, scrapePrompt + "\n")
    logf.close()

# Close the file we wrote out to.
# outFile.close()

# Now it's time to write the JSON of the semester information.
courseSemesters = parser.getSemesterListing()
jsonFileName = "json_semesters_" + courseInput + ".txt"
with open(jsonFileName, 'w') as jsonFile:
    json.dump(courseSemesters, jsonFile, indent=2)
jsonFile.close()

# In our case we want to just write this to the DB now.
# Currently app specification is total through the entire semester range.
# NOTE: This does not work right now. Program mentions that
# "ClassTotals.course_name" must be a "Courses" instance. This requires
# further discussion.
dictProfTotals = parser.getProfTotals()
# for prof in dictProfTotals:
#     try:
#         classTotal = ClassTotals(course_name=readableCourse,
#                                  prof_total=dictProfTotals[prof],
#                                  semester="All")
#         classTotal.save()
#     except:
#         print("Unexpected error with ClassTotals:", sys.exc_info()[0], dictProfTotals)

# Now it's time to write the JSON of professors for individual semesters.
dictSemesterProfs = parser.getSemesterProfs()
##jsonFileName = "json_profSemesters_" + courseInput + ".txt"
##with open(jsonFileName, 'w') as jsonFile:
##    json.dump(dictSemesterProfs, jsonFile, indent=2)
##jsonFile.close()

# Kill the webkit_server processes to prevent memory leak
# print("Killing webkit_server processes...")
# killWebkitServers()

# End
