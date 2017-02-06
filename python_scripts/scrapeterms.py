#!/usr/bin/python3

import dryscrape
from bs4 import BeautifulSoup
import time
import sys
import os
import json
from python_scripts.registrarparse import *
from python_scripts.terminfo import *
from python_scripts.cmdmanage import *
from se_site.registrar_analyzer.models import ClassTotals, Courses

# Parse and check command line arguments
if len(sys.argv) != 5:
    print("\nUsage:\n\tpython3 scrapeterms.py <start_semester> <end_semester> <course> <out_file>")
    print('Example:\n\tpython3 scrapeterms.py "Fall 2005" "Spring 2008" cp1 ./results/cp1.txt\n')
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
parser = RegistrarParser(startSemester, endSemester,
                         courseInput, outFilePath)
print(parser)

# Open the file
with open(outFilePath, 'w') as outFile:

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
    currentSemIndex = startTermIndex # Start counter for semester scraping
    courseUrl = parser.getCourseUrl() # Formatted course string for registrar

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
        semProfs = {} # Professor section count for this semester
        sections = [] # The list of course sections for this semester
        courseGroupDivs = parser.getCourseGroupDivs(responseSoup)
        for courseGroupDiv in courseGroupDivs:

            # With the group we can get individual sections.
            scrapePrompt = "\n>> Reached a group result."
            parser.writeStringToFile(outFile, scrapePrompt + "\n")
            courseSections = parser.getCourseSectionDivs(courseGroupDiv)
            i = 1 # Debugging Course Section Counter
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
                                meetList = parser.getSectionMeetingInfo(sectionMeetingDiv, semProfs)
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

        # Now add this semester's prof information to the semesterProfs list
        semesterProfsToAdd = []
        semesterProfsToAdd.append(numDict[currentTermNum])
        semesterProfsToAdd.append(semProfs)
        parser.addSemesterProfs(semesterProfsToAdd)

        # Also add the list of individual sections from this semester
        parser.addSectionListing(sections)

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
            timeAvg = timeSoFar/semsParsed
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

# Close the file we wrote out to.
outFile.close()

# Now it's time to write the JSON of the semester information.
courseSemesters = parser.getSemesterListing()
jsonFileName = "json_result_" + courseInput + ".txt"
with open(jsonFileName, 'w') as jsonFile:
    json.dump(courseSemesters, jsonFile, indent=2)
jsonFile.close()

# Kill the webkit_server processes to prevent memory leak
print("Killing webkit_server processes...")
killWebkitServers()

# End
