from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse
from django.views import generic, View

# Essential imports for getting DB data
import json
from django.core import serializers
from django.db.utils import IntegrityError
from django.db.models import Sum
from .models import Courses

# Stuff for Markup
from markupsafe import Markup

# Stuff for plotly
import plotly
from plotly.graph_objs import Bar, Layout, Figure

# Stuff for term info
from python_scripts.terminfo import *

course_options_array = [orderedSemesterList, sortedFullCourseNames]


# Create your views here.
class IndexView(View):

    template_name = 'registrar_analyzer/index.html'
    context_object_name = 'course_options_array' # Context variable

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'course_options_array': course_options_array})

    def post(self, request, *args, **kwargs):
        postInfo = {}

        if request.method == "POST":
            courseName = request.POST['courseNameSelect']
            startSemester = request.POST['startSemesterSelect']
            endSemester = request.POST['endSemesterSelect']
            graphType = request.POST['graphSelect']
            postInfo['courseNameSelect'] = courseName
            postInfo['startSemesterSelect'] = startSemester
            postInfo['endSemesterSelect'] = endSemester
            postInfo['graphSelect'] = graphType
            try:
                figureToGraph = getFigure(courseName, startSemester, endSemester, graphType)
                graphDiv = plotly.offline.plot(figureToGraph, output_type='div')
                return render(request, self.template_name,
                              {'postInfo': postInfo, 'course_options_array': course_options_array,
                               'div_placeholder': Markup(graphDiv)})
            except:
                htmlStr = "<p>Sorry, the semester range you specified has no data. " \
                          "You should specify the full range to see which range has data.</p>"
                return render(request, self.template_name,
                              {'postInfo': postInfo, 'course_options_array': course_options_array,
                               'div_placeholder': Markup(htmlStr)})
        else:
            return render(request, self.template_name,
                          {'course_options_array': course_options_array})


def getFigure(inputCourse, startSemester, endSemester, graphType):

    # Get course data
    semesterArray = []  # Semester info array that will store all semesters for a course
    semesterDict = {}  # Dictionary holding information for each semester entry
    allCourseSections = Courses.objects.filter(course_name=inputCourse)  # Get all entries for this course
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

    # Get the indices for the semester numbers. Here we assume the semester range
    # is valid because the form will be validated on submit.
    startTermNum = termDict[startSemester]
    startTermIndex = allSemesters.index(startTermNum)
    endTermNum = termDict[endSemester]
    endTermIndex = allSemesters.index(endTermNum)
    currentSemIndex = startTermIndex  # Start counter for semester scraping

    # We need to append the semesters in order now
    while currentSemIndex <= endTermIndex:
        currentSemNumStr = allSemesters[currentSemIndex]
        currentSemKey = numDict[currentSemNumStr]
        oneSemester = [currentSemKey]
        try:
            for val in semesterDict[currentSemKey]:
                oneSemester.append(val)
        except:
            # This case means we had missing data
            pass
        semesterArray.append(oneSemester)
        currentSemIndex += 1

    if graphType == "Bar":
        figure = makeBarFigure(inputCourse, semesterArray)
    elif graphType == "Pie":
        figure = makePieFigure(inputCourse, semesterArray, startSemester, endSemester)
    return figure


def makeBarFigure(inputCourse, semesterArray):
    # First pass-through:
    # 1.) Get instructor names into a dictionary where the
    #  key is instructor name, value is dict
    # 2.) Get semester names into a list
    courseProfs = {}
    courseSems = []
    for semester in semesterArray:
        if len(semester) == 1:
            courseSems.append(semester[0])
        else:
            for section in semester:
                if semester.index(section) == 0:
                    continue
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

    # Second pass-through:
    # For every section, see if the instructor matches a key
    # in the courseProfs dictionary. If it does, append a dictionary
    # With the following key/val pairs:
    # 'semester' key will have the semester name.
    # 'enroll' will have total enrollment count for this professor in this semester.
    for semester in semesterArray:
        if len(semester) == 1:
            continue
        else:
            for section in semester:
                if semester.index(section) == 0:
                    continue
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
        courseProfs[prof] = semEnrollDict  # Update with 0 counts

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
            x=courseSems,
            y=trace,
            name=profNamesList[profIndex]
        )
        data.append(barToAdd)
    layout = Layout(
        title=inputCourse + " Enrollment",
        barmode='stack'
    )

    figure = Figure(data=data, layout=layout)
    return figure


def makePieFigure(inputCourse, semesterArray, startSemester, endSemester):
    # First pass-through:
    # 1.) Get instructor names into a dictionary where the
    #  key is instructor name, value is section count
    profNames = {}
    for semester in semesterArray:
        if len(semester) == 1:
            continue
        else:
            for section in semester:
                if semester.index(section) == 0:
                    continue
                if section['creditValue'] == "0 Credits":
                    continue
                meetings = section['meetings']
                if len(meetings) == 0:
                    continue
                instructor = meetings[0]['instructor']
                if instructor not in profNames:
                    profNames[instructor] = 1
                else:
                    profNames[instructor] += 1

    # Second step: Get every key and value in the profNames dictionary
    # and append it as data for the pie graph
    profNameList = []
    profCounts = []
    for key in sorted(profNames):
        profNameList.append(key)
        profCounts.append(profNames[key])

    # Set the pie graph's data attributes
    data = [
        {
            "labels": profNameList,
            "values": profCounts,
            "hoverinfo": "label+value+percent",
            "textinfo": "value+percent",
            "type": "pie"
        }
    ]

    # Set the layout attributes of the bar graph, such as title.
    layout = Layout(
        title=inputCourse + " Professor Totals from " + startSemester + " to " + endSemester
    )

    # Combine the data and layout into a figure.
    figure = Figure(data=data, layout=layout)
    return figure
# End
