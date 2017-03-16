import os
import sys
import json

# Stuff for plotly
import plotly
from plotly.graph_objs import Bar, Layout, Figure

# Stuff for term information
from terminfo import *

# Import settings for django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "se_site.settings.dev")
import django
from django.core import serializers
from django.db.utils import IntegrityError

django.setup()
from registrar_analyzer.models import Courses

# Parse and check command line arguments
if len(sys.argv) != 4:
    print("\nUsage:\n\tpython dbrequest.py <course> <startSemester> <endSemester>")
    print('Example:\n\tpython dbrequest.py ' +
          '"Analysis of Algorithms" "Fall 2005" "Spring 2008"\n')
    exit()

inputCourse = sys.argv[1]
startSemester = sys.argv[2]
endSemester = sys.argv[3]
print("Start Semester: " + startSemester)
print("End Semester: " + endSemester)

# Semester info array that will store all semesters for a course
semesterArray = []

# Dictionary holding information for each semester entry
semesterDict = {}

# Get OPL course data
allCourseSections = Courses.objects.filter(course_name=inputCourse)
serialData = serializers.serialize("json", allCourseSections)
jsonArr = json.loads(serialData)
for result in jsonArr:

    # This is where we take the 'fields' key
    # And then construct objects for each semester
    fieldsJson = result['fields']
    barGraphDict = {}
    semester = fieldsJson['semester']


    # Add simple entries first
    barGraphDict['creditValue'] = fieldsJson['credit_value']
    barGraphDict['course'] = fieldsJson['course_name']
    barGraphDict['enrollNow'] = fieldsJson['enroll_now']
    barGraphDict['enrollMax'] = fieldsJson['enroll_max']
    barGraphDict['honors'] = fieldsJson['honors']
    barGraphDict['semester'] = semester

    # Now for the more involved entries in the meeting
    meetingInfo = {}
    meetingInfo['instructor'] = fieldsJson['instructor']
    meetingInfo['room'] = fieldsJson['room']
    meetingInfo['days'] = fieldsJson['meeting_days']
    meetingInfo['timeStart'] = fieldsJson['time_start']
    meetingInfo['timeEnd'] = fieldsJson['time_end']

    # Put the meeting info dictionary into the meetings array
    barGraphDict['meetings'] = [meetingInfo]

    if semester not in semesterDict:
        semesterDict[semester] = [barGraphDict]
    else:
        semesterDict[semester].append(barGraphDict)

# First we need to find the end and start semester. Start by
# Comparing numeric values first
lowestKey = 9999
highestKey = 0
for semKey in semesterDict:
    termNum = int(termDict[semKey])
    if termNum < lowestKey:
        lowestKey = termNum
    if termNum > highestKey:
        highestKey = termNum
lowestKey = str(lowestKey)
highestKey = str(highestKey)

# Get the indices for the semester numbers. Here we assume the semester range
# is valid because the form will be validated on submit.
startTermNum = termDict[startSemester]
startTermIndex = allSemesters.index(startTermNum)
endTermNum = termDict[endSemester]
endTermIndex = allSemesters.index(endTermNum)
currentSemIndex = startTermIndex # Start counter for semester scraping

# We need to append the semesters in order now
while currentSemIndex <= endTermIndex:
    currentSemNumStr = allSemesters[currentSemIndex]
    currentSemKey = numDict[currentSemNumStr]
    oneSemester = []
    for val in semesterDict[currentSemKey]:
        oneSemester.append(val)
    semesterArray.append(oneSemester)
    currentSemIndex += 1

"""
Getting here means we have all semesters to graph.
Now it's time for the plotly stuff.
"""
# First pass-through:
# 1.) Get instructor names into a dictionary where the
#  key is instructor name, value is dict
# 2.) Get semester names into a list
courseProfs = {}
courseSems = []
for semester in semesterArray:
    if len(semester) == 0:
        continue
    else:
        for section in semester:
            if section['creditValue'] == "0 Credits":
                continue
            semName = section['semester']
            if semName not in courseSems:
                courseSems.append(semName)
            meetings = section['meetings']
            if len(meetings) == 0:
                continue
            instructor = meetings[0]['instructor']
            if instructor not in courseProfs:
                courseProfs[instructor] = {}
# print("\nFIRST PASS-THROUGH")
# print("Course Professors: " + str(courseProfs))
# print("Course Semesters: " + str(courseSems))

# Second pass-through:
# For every section, see if the instructor matches a key
# in the courseProfs dictionary. If it does, append a dictionary
# With the following key/val pairs:
# 'semester' key will have the semester name.
# 'enroll' will have total enrollment count for this professor in this semester.
for semester in semesterArray:
    if len(semester) == 0:
        continue
    else:
        for section in semester:
            if section['creditValue'] == "0 Credits":
                continue
            semName = section['semester']
            meetings = section['meetings']
            if len(meetings) == 0:
                continue
            instructor = meetings[0]['instructor']
            enroll = int(section['enrollNow'])
            if semName not in courseProfs[instructor]:
                courseProfs[instructor][semName] = enroll
            else:
                courseProfs[instructor][semName] += enroll
# print("\nSECOND PASS-THROUGH")
# print("Professor Enrollment Semester Counts: " + str(courseProfs))

# Third part: Use courseSems list to get enrollment data in order for
# All the different professors
# 1.) Get all the professor names (keys in courseProfs)
# 2.) Fill in missing semesters with 0 enrollment for that professor
profNamesList = []
for key in sorted(courseProfs):
    profNamesList.append(key)
for prof in profNamesList:
    semEnrollDict = courseProfs[prof]
    for sem in courseSems:
        if sem not in semEnrollDict:
            semEnrollDict[sem] = 0
    courseProfs[prof] = semEnrollDict # Update with 0 counts

# Fourth part: Create bar graph info for each professor
# 1.) Go in order of semester
# 2.) Append the enrollment for each semester for the professor,
# then add it as a list. This means we have a 2D list
traces = []
for prof in profNamesList:
    enrollCountList = []
    for sem in courseSems:
        semEnrolled = courseProfs[prof][sem]
        enrollCountList.append(semEnrolled)
    traces.append(enrollCountList)

# Fifth part: Now create the Bar objects
data = []
for trace in traces:
    profIndex = traces.index(trace)
    barToAdd = Bar(
        x = courseSems,
        y = trace,
        name = profNamesList[profIndex]
    )
    data.append(barToAdd)
layout = Layout(
    title = inputCourse + " Enrollment",
    barmode = 'stack'
)

figure = Figure(data=data, layout=layout)

plotly.offline.plot(
    figure,
    filename = "./bar-stacked-enrollment.html"
)



#