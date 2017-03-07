from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Courses

from python_scripts.terminfo import *

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'registrar_analyzer/index.html'
    context_object_name = 'course_options_array' # Context variable

    def get_queryset(self):
        """ Get the last 5 course info """
        return [orderedSemesterList, sortedFullCourseNames]

