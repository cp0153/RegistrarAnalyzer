from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse
from django.views import generic

from .models import Courses

from python_scripts.terminfo import *
course_options_array = [orderedSemesterList, sortedFullCourseNames]

# Create your views here.
class IndexView(generic.ListView):

    template_name = 'registrar_analyzer/index.html'
    context_object_name = 'course_options_array' # Context variable


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
            return render(request, self.template_name,
                          {'postInfo': postInfo, 'course_options_array': course_options_array})
        else:
            return render(request, self.template_name,
                          {'course_options_array': course_options_array})


    def get_queryset(self):
        """ Get the last 5 course info """
        return course_options_array

"""
def index(request):
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
    return render(request, 'registrar_analyzer/index.html', postInfo)
"""

# End