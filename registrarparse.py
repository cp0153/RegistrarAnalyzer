####################################
# DICTIONARIES WITH PROFESSOR INFO #
####################################

# Nothing here

####################################
# FUNCTIONS AND PARSING            #
####################################

def getCourseGroupDivs(soup):
    """
    This function gets the entire group of section results for one course
    into a list.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        The parsed HTML of the response in a BeautifulSoup object.

    Returns
    -------
    list
        A list of bs4.element.Tag objects representing entire groups of
        section results. This list is usually 1 in length.

    """
    return soup.select("div.class-schedule-search-results-group-results")

def getCourseSectionDivs(groupDivTag):
    """
    This function gets all sections for one course into a list.

    Parameters
    ----------
    groupDivTag : Tag
        The Group Div for an entire course.

    Returns
    -------
    ResultSet
        A ResultSet of Tag objects representing individual class sections.

    """
    return groupDivTag.find_all('div', attrs = {'class': 'class-schedule-search-result'})

def isCancelled(sectionTag):
    """
    This function checks to see if the individual course section
    is a cancelled section.

    Parameters
    ----------
    sectionTag : Tag
        The single course section div.

    Returns
    -------
    boolean
        True if the section is found to be cancelled, False if the section
        is not cancelled.

    """
    topPart = sectionTag.find('div', attrs = {'class': 'inside'})
    cancelled = topPart.find("i", attrs = {'class': 'fa-times-circle'})
    if cancelled is not None:
        return True
    else:
        return False
    

def getDetailsDiv(sectionTag):
    """
    This function gets the div with all the class section details.

    Parameters
    ----------
    sectionTag : Tag
        The single course section div.

    Returns
    -------
    Tag
        The div with all the inner class section details as a Tag.

    """
    return sectionTag.find('div', attrs = {'class': 'details'})

def getMeetingInfoDivs(sectionDetailsTag):
    """
    This function gets the meeting info divs at the bottom of the section
    details div. THIS DOES NOT EXTRACT THE SPECIFIC CLASS INFO.

    Parameters
    ----------
    sectionDetailsTag : Tag
        The div with all the inner class section details as a Tag.
        This is retrieved by getDetailsDiv().

    Returns
    -------
    ResultSet
        A ResultSet of Tag objects representing individual meeting info divs.
    None
        The NoneType object is returned if no meeting info was found.

    """
    classMeetingDivs = sectionDetailsTag.find('div', attrs = {'class': 'class-meetings'})
    if classMeetingDivs is None:
        return None
    else:
        return classMeetingDivs.find_all('div', attrs = {'class': 'section-meeting'})

def getSectionMeetingInfo(meetingInfoDiv, semProfDict):
    """
    This function extracts specific info from a meeting info div.
    The usual case is that there are 5 divs of information, where:
    - [0] (first div) is Days the class meets, e.g. MWF
    - [1] (second div) is Times the class meets, e.g. 10:00 AM - 10:50 AM
    - [2] (third div) is session period, e.g. 9/2/2009 - 12/15/2009
    - [3] (fourth div) is Instructor
    - [4] (fifth div) is Room Number
    Note that even though there are five divs, the returned dictionary
    has seven keys; the times and session are split into two parts.

    Parameters
    ----------
    meetingInfoDiv : Tag
        The div with the meeting details. The inner divs have specific info.
    semProfDict: dict
        A dictionary that contains the instructor names as keys, and how
        many sections they taught in the current semester being parsed.

    Returns
    -------
    list
        The list returned has two items.
        - The first item is a dictionary with 7 key/value pairs:
        'days', 'timeStart', 'timeEnd', 'sessionStart',
        'sessionEnd', 'instructor', 'room'
        - The second item is an updated dictionary containing the instructor
        names as keys, and how many sections they taught in the semester
        as an integer value.

    """

    # In these two base cases, this means there was no meeting info.
    if meetingInfoDiv is None:
        return {}
    meetingCells = meetingInfoDiv.find_all("div")
    if meetingCells is None:
        return {}

    # Get the individual divs for each piece of meeting information.
    daysCell = meetingCells[0]
    timesCell = meetingCells[1]
    sessionCell = meetingCells[2]
    instructorCell = meetingCells[3]
    roomCell = meetingCells[4]

    # Get the days
    daySpans = daysCell.find_all('span')
    days = daySpans[3].getText()

    # Get the times
    timeSpans = timesCell.find_all('span')
    timeStart = timeSpans[1].getText()
    timeEnd = timeSpans[3].getText()

    # Get the session
    sessionSpans = sessionCell.find_all('span')
    sessionStart = sessionSpans[1].getText()
    sessionEnd = sessionSpans[2].getText()
    sessionEnd = sessionEnd.replace(' ', '').replace('–', '')

    # Get the instructor
    instructorSpans = instructorCell.find_all('span')
    instructor = instructorSpans[2].getText()
    if instructor not in semProfDict:
        semProfDict[instructor] = 1
    else:
        semProfDict[instructor] += 1

    # Get the room
    roomSpans = roomCell.find_all('span')
    room = roomSpans[2].getText()

    # Now we can create the dictionary and return it.
    meetInfoDict = {}
    meetInfoDict['days'] = days
    meetInfoDict['timeStart'] = timeStart
    meetInfoDict['timeEnd'] = timeEnd
    meetInfoDict['sessionStart'] = sessionStart
    meetInfoDict['sessionEnd'] = sessionEnd
    meetInfoDict['instructor'] = instructor
    meetInfoDict['room'] = room
    return [meetInfoDict, semProfDict]

def getQuickInfoDetails(sectionDetailsTag):
    """
    This function parses the sidebar div that has the "Quick Info" section,
    which describes enrollment numbers, credits, and if the class is Honors.
    
    First, this function looks for the text-section divs. There are two cases.
    1.) There are Enrollment Requirements Listed 
    - [0] is Course Description
    - [1] is Enrollment Requirements
    - [2] is "Quick Info" (enrollment number, credits, if class is honors)
    - There are more text-sections after this, but we don't care about them.
    2.) There are no Enrollment Requirements listed
    - [0] is Course Description
    - [1] is "Quick Info" section

    Then with the "Quick Info" div, there are 3 guaranteed div.text elements:
    - [0] gives enrollment numbers.
    - [1] gives "Regular Academic Session"
    - [2] gives credits worth

    Parameters
    ----------
    sectionDetailsTag : Tag
        The div with all the inner class section details as a Tag.
        This is retrieved by getDetailsDiv().

    Returns
    -------
    dict
        The dictionary with 4 pieces of info as key/value pairs:
        - 'enrollNow', 'enrollMax', 'creditValue', 'honors'

    """

    # First find the Quick Info div
    if sectionDetailsTag is None:
        return {}
    textSectionDivs = sectionDetailsTag.find_all('div', attrs = {'class': 'text-section'})
    if textSectionDivs is None:
        return {}

    # We need to check if there is an enrollment requirements section.
    quickInfoDiv = textSectionDivs[2]
    usersIcon = quickInfoDiv.find("i", attrs = {'class': 'fa-users'})
    if usersIcon is None:
        quickInfoDiv = textSectionDivs[1]
    
    # Now we can look for the quick info inside.
    textDivs = quickInfoDiv.find_all('div', attrs = {'class': 'text'})
    enrollDiv = textDivs[0]
    creditsDiv = textDivs[2]
    
    # Now get the enrollment numbers
    enrollNow = enrollDiv.find('strong').getText()
    enrollSpans = enrollDiv.find_all('span')
    enrollMax = enrollSpans[2].getText()

    # Now get the credit amount
    creditsSpans = creditsDiv.find_all('span')
    creditValue = creditsSpans[3].getText()

    # Check if this class is an honors section
    honors = 'No'
    honorsIcon = quickInfoDiv.find("i", attrs = {'class': 'fa-star'})
    if honorsIcon is not None:
        honors = 'Yes'

    # Now we can create the dictionary to return.
    qInfoDict = {}
    qInfoDict['enrollNow'] = enrollNow
    qInfoDict['enrollMax'] = enrollMax
    qInfoDict['creditValue'] = creditValue
    qInfoDict['honors'] = honors
    return qInfoDict

def printMeetingInfoDict(meetInfoDict):
    """
    This function prints out the meeting info for a course section
    in a more human-readable format.

    Parameters
    ----------
    meetInfoDict : dict
        The dictionary with the meeting info for the class section.
    """
    if meetInfoDict is None:
        print("> No meeting info found.")
    else:
        print("> Meeting Days:   " + meetInfoDict['days'])
        print("> Time Start:     " + meetInfoDict['timeStart'])
        print("> Time End:       " + meetInfoDict['timeEnd'])
        print("> Session Start:  " + meetInfoDict['sessionStart'])
        print("> Session End:    " + meetInfoDict['sessionEnd'])
        print("> Instructor:     " + meetInfoDict['instructor'])
        print("> Room:           " + meetInfoDict['room'])

def printQuickInfoDict(qInfoDict):
    """
    This function prints out the quick info for a course section
    in a more human-readable format.

    Parameters
    ----------
    qInfoDict : dict
        The dictionary with the quick info for the class section.
    """
    if qInfoDict is None:
        print("> No enrollment, credit, or honors info found.")
    else:
        print("> Enrolled Now:   " + qInfoDict['enrollNow'])
        print("> Enrollment Max: " + qInfoDict['enrollMax'])
        print("> Credit Value:   " + qInfoDict['creditValue'])
        print("> Honors Section: " + qInfoDict['honors'])

# End
