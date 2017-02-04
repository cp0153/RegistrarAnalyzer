import json
import sys
import plotly
from plotly.graph_objs import Layout, Figure

# Parse and check command line arguments
if len(sys.argv) != 4:
    print("\nUsage:\n\tpython3 proftotalpie.py <prof_total_json> <course_long> <course_short>")
    print('Example:\n\tpython3 proftotalpie.py ' +
          'samples/prof_totals/json_profTotals_cp3.txt ' +
          '"Computing III" cp3\n')
    exit()

jsonPath = sys.argv[1]
courseLong = sys.argv[2]
courseShort = sys.argv[3]

# Read in the JSON
with open(jsonPath) as jsonFile:
    jsonData = json.load(jsonFile)
jsonFile.close()

# Make lists for both the professor keys and their respective values.
profNames = []
profCounts = []
for key in sorted(jsonData):
    profNames.append(key)
    profCounts.append(jsonData[key])

# Set the bar graph's data.
data = [
    {
        "labels": profNames,
        "values": profCounts,
        "hoverinfo": "label+value+percent",
        "textinfo": "value+percent",
        "type": "pie"     
    }
]

# Set the layout attributes of the bar graph, such as title.
layout = Layout(
    title = courseLong+" Professor Totals Fall 2000 to Spring 2017"
)

# Combine the data and layout into a figure.
figure = Figure(data=data, layout=layout)

# Create the HTML file.
plotly.offline.plot(
    figure,
    filename = "./graphs/pie/pie-plot-" + courseShort + ".html"
)
