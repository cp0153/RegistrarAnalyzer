import json
import sys
import plotly
from plotly.graph_objs import Bar, Layout, Figure

# Parse and check command line arguments
if len(sys.argv) != 3:
    print("\nUsage:\n\tpython3 enrollbar.py <semester_json> <course_short>")
    print('Example:\n\tpython3 enrollbar.py ' +
          'samples/semesters/json_semesters_cp1.txt cp1\n')
    exit()

jsonPath = sys.argv[1]
courseShort = sys.argv[2]

# Read in the JSON
with open(jsonPath) as jsonFile:
    jsonData = json.load(jsonFile)
jsonFile.close()

# Make lists for both the professor keys and their respective values.
semEnrollments = []
semNames = []
courseName = "No Course"
for semester in jsonData:
    semEnrollment = 0
    if len(semester) == 0:
        continue
    else:
        for section in semester:
            if section['creditValue'] != "0 Credits":
                semEnrollment += int(section['enrollNow'])
            semName = section['semester']
            courseName = section['course']
        semEnrollments.append(semEnrollment)
        semNames.append(semName)

# Set the bar graph's data.
data = [
    Bar(x=semNames,
        y=semEnrollments,
        opacity=0.6)
]

# Set the layout attributes of the bar graph, such as title.
layout = Layout(
    title = courseName + " Enrollment from Fall 2000 to Spring 2017"
)

# Combine the data and layout into a figure.
figure = Figure(data=data, layout=layout)

# Create the HTML file.
plotly.offline.plot(
    figure,
    filename = "./graphs/bar/bar-enrollment-" + courseShort + ".html"
)
