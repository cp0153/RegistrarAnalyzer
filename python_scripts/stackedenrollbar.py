import json
import sys
import plotly
from terminfo import *
from plotly.graph_objs import Bar, Layout, Figure

# Parse and check command line arguments
if len(sys.argv) != 3:
    print("\nUsage:\n\tpython3 stackedenrollbar.py <semester_json> <course_short>")
    print('Example:\n\tpython3 stackedenrollbar.py ' +
          'samples/semesters/json_semesters_opl.txt opl\n')
    exit()

jsonPath = sys.argv[1]
courseShort = sys.argv[2]
readableCourseName = courseNameDict[courseShort]

# Read in the JSON
with open(jsonPath) as jsonFile:
    jsonData = json.load(jsonFile)
jsonFile.close()

# First pass-through:
# 1.) Get instructor names into a dictionary where the
#  key is instructor name, value is dict
# 2.) Get semester names into a list
courseProfs = {}
courseSems = []
for semester in jsonData:
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
print("\nFIRST PASS-THROUGH")
print("Course Professors: " + str(courseProfs))
print("Course Semesters: " + str(courseSems))

# Second pass-through:
# For every section, see if the instructor matches a key
# in the courseProfs dictionary. If it does, append a dictionary
# With the following key/val pairs:
# 'semester' key will have the semester name.
# 'enroll' will have total enrollment count for this professor in this semester.
for semester in jsonData:
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
print("\nSECOND PASS-THROUGH")
print("Professor Enrollment Semester Counts: " + str(courseProfs))

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
    title = readableCourseName + " Enrollment",
    barmode = 'stack'
)

figure = Figure(data=data, layout=layout)

plotly.offline.plot(
    figure,
    filename = "./graphs/bar/bar-stacked-enrollment-" + courseShort + ".html"
)


### Set the bar graph's data.
##data = [
##    Bar(x=semNames,
##        y=semEnrollments,
##        opacity=0.6)
##]
##
### Set the layout attributes of the bar graph, such as title.
##layout = Layout(
##    title = courseName + " Enrollment"
##)
##
### Combine the data and layout into a figure.
##figure = Figure(data=data, layout=layout)
##
### Create the HTML file.
##plotly.offline.plot(
##    figure,
##    filename = "./graphs/bar/bar-short-enrollment-" + courseShort + ".html"
##)
