#!/usr/bin/python3

import dryscrape
from bs4 import BeautifulSoup
import time
from registrarparse import *
from terminfo import *
from cmdmanage import *

####################################
# USER PROMPT AND URL REQUEST      #
####################################

# Now prompt the user for the term they want
print("> This program will scrape a range of semesters.")
print("> Please enter the starting semester, followed by the year.")
startSemester = input("Example is 'Fall 2013' or 'Spring 2014': ")
print("> Please enter the ending semester, followed by the year.")
endSemester = input("Examples are Fall 2016 or Spring 2017: ")
print("Please enter the course you want to scrape.")
courseInput = input("cp1, cp2, cp3, cp4, assembly, opl, foundations, "
                    "arch, os, algorithms, ai, compiler, cg2, cg1, "
                    "cv, cybercrime, dc1, dc2, datamining, db1, db2, "
                    "gui1, gui2, ml, mobileapp2, mobilerobotics1, "
                    "mobilerobotics2, nlp, selected, se1, se2, special: ")

# Tell the user which course they're scraping and which semesters
print("\n> You chose to scrape the course " + courseNameDict[courseInput])
print("> You chose to scrape semesters " + startSemester + " through " + endSemester)

# Get the indices for the semester numbers
beginning = time.time()
startTermNum = termDict[startSemester]
startTermIndex = allSemesters.index(startTermNum)
endTermNum = termDict[endSemester]
endTermIndex = allSemesters.index(endTermNum)
##print("\nallSemesters length is " + str(len(allSemesters)))
##print(startTermNum + " is index " + str(startTermIndex))
##print(endTermNum + " is index " + str(endTermIndex))

# Set up necessary variables for scraping
currentSemIndex = startTermIndex # Start counter for semester scraping
courseTitle = courseDict[courseInput] # Formatted course string for registrar
semesterProfs = [] # Information about professors for all scraped semesters.
session = dryscrape.Session() # Start dryscrape session

# This while loop goes through the range of semesters specified
while currentSemIndex <= endTermIndex:

    # Form the URL.
    currentTermNum = allSemesters[currentSemIndex]
    scrapeUrl = createRegistrarUrl(currentTermNum, courseTitle)
    print("\n>>> Getting Info for Semester " + numDict[currentTermNum])

    # Now that we have the user input, request the URL.
    responseSoup = getSiteBody(session, scrapeUrl, 5)
    semProfs = {} # Professor section count for this semester
    courseGroupDivs = getCourseGroupDivs(responseSoup)
    for courseGroupDiv in courseGroupDivs:

        print("\n>> Reached a group result.")

        # Now we have the group, and with that group we can get individual sections.
        courseSections = getCourseSectionDivs(courseGroupDiv)
        i = 1 # Debugging Course Section Counter
        for courseSection in courseSections:

            # Before moving on, check if there is a "Cancelled Section" icon
            # If there is then there's no point in continuing
            print("\n>> Parsing Course Section " + str(i))
            if isCancelled(courseSection) is True:
                print("> This course section is cancelled.")
                i += 1
            else:

                # We need the section details div before proceeding.
                sectionDetailsDiv = getDetailsDiv(courseSection)
                
                # From the section details, find quick info first
                try:
                    quickDict = getQuickInfoDetails(sectionDetailsDiv)
                    printQuickInfoDict(quickDict)
                except:
                    print("> Something went wrong trying to get quick info for this section."
                          " There was probably no quick info listed.")

                # From section details, search for meeting info
                try:

                    # It's possible there are no results for meeting info
                    meetingInfoDivs = getMeetingInfoDivs(sectionDetailsDiv)
                    if meetingInfoDivs is None:
                        print("> This course section has no meeting information.")
                    else:
                        for sectionMeetingDiv in meetingInfoDivs:

                            # So now that we've gotten an individual meeting info tag,
                            # get the five pieces of information from it
                            meetList = getSectionMeetingInfo(sectionMeetingDiv, semProfs)
                            meetDict = meetList[0]
                            semProfs = meetList[1]
                            printMeetingInfoDict(meetDict)
                except:
                    print("> Something went wrong trying to get meeting info for this section."
                          " There were probably zero meeting sections listed.")
                i += 1

    # Now add this semester's information to the semesterProfs list
    # Make sure we indicate for each list element that the first element is
    # A string saying the course term, and the second element is the dict
    semesterProfsToAdd = []
    semesterProfsToAdd.append(numDict[currentTermNum])
    semesterProfsToAdd.append(semProfs)
    semesterProfs.append(semesterProfsToAdd)

    # Move on to the next semester.
    currentSemIndex += 1

# We've parsed all semesters, print out the data in collective semesters
print("\n>>> Now printing out " + startSemester + " through " + endSemester
      + " for " + courseNameDict[courseInput])
printSemesterProfs(semesterProfs)
        
# Now go through the semesterProfs dictionary and get a total prof count
profTotals = getProfTotals(semesterProfs)
print("\n>>> Professor Totals for " + courseNameDict[courseInput]
      + " for semesters " + startSemester + " through " + endSemester)
for prof in profTotals:
    print("> " + prof + ": " + str(profTotals[prof]))

# Print how long this took.
finished = time.time()
runningTime = round(finished - beginning, 3)
print("!!! All of this took " + str(runningTime) + " seconds.")

# Kill the webkit_server processes to prevent memory leak
print("Killing webkit_server processes...")
killWebkitServers()

# End
