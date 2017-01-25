#!/usr/bin/python3

import dryscrape
from bs4 import BeautifulSoup
import time
from registrarparse import *
from terminfo import *

SLEEP_TIME = 5

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
print("\nallSemesters length is " + str(len(allSemesters)))
print(startTermNum + " is index " + str(startTermIndex))
print(endTermNum + " is index " + str(endTermIndex))

# Have a counter to start at the start index, and then a while loop
currentSemIndex = startTermIndex

# Information about professors.
semesterProfs = []

while currentSemIndex <= endTermIndex:

    # Form the URL.
    scrapeUrlBase = "https://www.uml.edu/student-dashboard/#my-academics/class-schedule/search?term="
    courseTitle = courseDict[courseInput]
    currentTermNum = allSemesters[currentSemIndex]
    scrapeUrlWithTerm = scrapeUrlBase + currentTermNum + "&courseTitle="
    scrapeUrl = scrapeUrlWithTerm + courseTitle
    print("\n>>> Getting Info for Semester " + numDict[currentTermNum])

    # Now that we have the user input, request the URL.
    session = dryscrape.Session()
    session.visit(scrapeUrl)
    time.sleep(SLEEP_TIME) # We need to wait for the javascript to render the classes.
    response = session.body()
    responseSoup = BeautifulSoup(response, "html.parser")
    responseSoup.prettify()

    # For this semester, make a temporary dictionary for the professors
    # and how many sections they taught this semester
    semProfs = {}

    # First step is getting the course group div elements.
    # For now I just select the first element. Later on this will be in a loop
    courseGroupDivs = getCourseGroupDivs(responseSoup)
    for courseGroupDiv in courseGroupDivs:

        print("\n>> Reached a group result.")

        # Now we have the group, and with that group we can get individual sections.
        # Take the first section and get the details (meeting time, date, etc.)
        # Get the first course section div/Tag and find its meeting info.
        # For now I just select the first element. Later on this will be in a loop
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

                sectionDetailsDiv = getDetailsDiv(courseSection)
                
                # From the section details, find enrollment info first
                try:
                    quickDict = getQuickInfoDetails(sectionDetailsDiv)
                    printQuickInfoDict(quickDict)
                except:
                    print("> Something went wrong trying to get quick info for this section."
                          " There was probably no quick info listed.")

                # From section details, search for meeting info
                # It's possible there are no results for this
                try:
                    meetingInfoDivs = getMeetingInfoDivs(sectionDetailsDiv)
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

# Now that we've parsed all semesters,
# print out the data in collective semesters
print("\n>>> Now printing out " + startSemester + " through " + endSemester
      + " for " + courseNameDict[courseInput])
for sem in semesterProfs:
    print("\n>> Printing out professor count for semester " + sem[0])
    semDict = sem[1]
    for prof in sorted(semDict):
        print("> " + prof + ": " + str(semDict[prof]))
        
# Now go through the semesterProfs dictionary and get a total prof count
profTotals = {}
for sem in semesterProfs:
    semDict = sem[1]
    for prof in semDict:
        if prof not in profTotals:
            profTotals[prof] = semDict[prof]
        else:
            profTotals[prof] += semDict[prof]

print("\n>>> Professor Totals for " + courseNameDict[courseInput]
      + " for semesters " + startSemester + " through " + endSemester)
for prof in profTotals:
    print("> " + prof + ": " + str(profTotals[prof]))

# Print how long this took.
finished = time.time()
runningTime = round(finished - beginning, 3)
print("!!! All of this took " + str(runningTime) + " seconds.")

# End
