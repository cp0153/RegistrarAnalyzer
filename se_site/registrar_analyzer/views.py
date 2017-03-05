from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Courses

numDict = {}
numDict['1010'] = 'Fall 2000'
numDict['1030'] = 'Spring 2001'
numDict['1110'] = 'Fall 2001'
numDict['1130'] = 'Spring 2002'
numDict['1210'] = 'Fall 2002'
numDict['1230'] = 'Spring 2003'
numDict['1310'] = 'Fall 2003'
numDict['1330'] = 'Spring 2004'
numDict['1410'] = 'Fall 2004'
numDict['1430'] = 'Spring 2005'
numDict['1510'] = 'Fall 2005'
numDict['1530'] = 'Spring 2006'
numDict['1610'] = 'Fall 2006'
numDict['1630'] = 'Spring 2007'
numDict['1710'] = 'Fall 2007'
numDict['1730'] = 'Spring 2008'
numDict['1810'] = 'Fall 2008'
numDict['1830'] = 'Spring 2009'
numDict['1910'] = 'Fall 2009'
numDict['1930'] = 'Spring 2010'
numDict['2010'] = 'Fall 2010'
numDict['2030'] = 'Spring 2011'
numDict['2110'] = 'Fall 2011'
numDict['2130'] = 'Spring 2012'
numDict['2210'] = 'Fall 2012'
numDict['2230'] = 'Spring 2013'
numDict['2310'] = 'Fall 2013'
numDict['2330'] = 'Spring 2014'
numDict['2410'] = 'Fall 2014'
numDict['2430'] = 'Spring 2015'
numDict['2510'] = 'Fall 2015'
numDict['2530'] = 'Spring 2016'
numDict['2610'] = 'Fall 2016'
numDict['2630'] = 'Spring 2017'

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'registrar_analyzer/index.html'
    context_object_name = 'course_options_list' # Context variable

    def get_queryset(self):
        """ Get the last 5 course info """
        return numDict

