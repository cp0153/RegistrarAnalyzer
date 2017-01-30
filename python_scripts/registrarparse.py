import dryscrape
from bs4 import BeautifulSoup
import time
from terminfo import *

class RegistrarParser(object):
    """
    Class that covers everything related to scraping the UML registrar.
    This class holds information for one course.
    """

    def __init__(self, startSem, endSem, crs, filePath):
        """
        Parameters
        ----------
        startSem : str
            The human-readable starting semester entered as an argument.
        endSem : str
            The human-readable end semester entered as an argument.
        crs : str
            The abbreviated course entered as an argument.
        filePath : str
            The path to the file to be written out to.
        """
        self.startSemester = startSem
        self.endSemester = endSem
        self.courseShort = crs
        self.outFilePath = filePath

        self.startTermNum = termDict[self.startSemester]
        self.endTermNum = termDict[self.endSemester]
        self.courseLong = courseNameDict[self.courseShort]
        self.courseUrl = courseDict[self.courseShort]

        self.semesterProfs = [] # Professor information for the semesters
        self.profTotals = {} # Total section counts for all professors
        self.semesters = [] # Info for each semester
        self.session = dryscrape.Session()
        
    def __str__(self):
        return """>>> REGISTRAR PARSER INFORMATION
- Start Semester: {}
- Start Term Number: {}
- End Semester: {}
- End Term Number: {}
- Course Name (Short): {}
- Course Name (Long): {}
- Course Registrar URL: {}
- Output File: {}""" \
        .format(self.startSemester, self.startTermNum,
                self.endSemester, self.endTermNum,
                self.courseShort, self.courseLong, self.courseUrl,
                self.outFilePath)

    def getReadableCourseName(self):
        return self.courseLong

    def getCourseUrl(self):
        return self.courseUrl

    def addSemesterProfs(self, semProfsToAdd):
        self.semesterProfs.append(semProfsToAdd)

    def calculateProfTotals(self):
        """
        This function calculates the total number of sections every
        professor instructed for a course in the semesters requested.
        When it comes to the structure of semestersProfs, it is a
        list where each element is a list of two elements:
        - [0] is the course term as a human readable string
        - [1] is the dict with every professor for that semester

        It should also be noted that the profTotals dictionary has
        the professor names as keys, and their total section count
        as an int value.
        """
        self.profTotals = {}
        for sem in self.semesterProfs:
            semDict = sem[1]
            for prof in semDict:
                if prof not in self.profTotals:
                    self.profTotals[prof] = semDict[prof]
                else:
                    self.profTotals[prof] += semDict[prof]

    def addSectionListing(self, sectionList):
        """
        This function adds a list of individual sections found for
        one semester into the parser's list of semesters.

        Parameters
        ----------
        sectionList : list
            The list where each element is a dictionary that contains
            both quick info and a list of all meeting info for each
            individual course section.
        """
        self.semesters.append(sectionList)

    def getSemesterListing(self):
        return self.semesters

    ####################################
    # FUNCTIONS AND PARSING            #
    ####################################

    def createRegistrarUrl(self, termNum, courseTitle):
        """
        This function creates the URL to visit for a specific semester and
        course on the Registrar Class-Schedule site.

        Parameters
        ----------
        termNum : str
            The term number for the semester as a string. This is an integer
            in string form.
        courseTitle : str
            The name of the course that is formatted in a way to work in the
            URL for the registrar.

        Returns
        -------
        str
            The full URL to scrape on one semester for one course.
        """
        scrapeUrlBase = "https://www.uml.edu/student-dashboard/"
        scrapeUrlBase += "#my-academics/class-schedule/search?term="
        scrapeUrlWithTerm = scrapeUrlBase + termNum + "&courseTitle="
        scrapeUrl = scrapeUrlWithTerm + courseTitle
        return scrapeUrl

    def getSiteBody(self, scrapeUrl, sleepSec):
        """
        This function gets the HTML contents of a session body after
        the page's javascript has rendered the page elements. Note that
        in order for a page to properly create its elements if driven by
        javascript, an appropriate sleep time needs to be passed.

        Parameters
        ----------
        session : dryscrape.Session
            The dryscrape Session object that will be used to visit the URL.
        scrapeUrl : str
            The full URL to the page to scrape.
        sleepSec : int
            The number of seconds to wait before getting the session body.
            For the UML Registrar, 5 seconds has been a reliable number.

        Returns
        -------
        bs4.BeautifulSoup
            The returned BeautifulSoup object will have the response body
            from the session run through an HTML parser.
        """
        self.session.visit(scrapeUrl)
        time.sleep(sleepSec) # Wait for the javascript to render the classes.
        response = self.session.body()
        self.session.reset() # Reset session to prevent memory leak
        soup = BeautifulSoup(response, "html.parser")
        return soup

    def getCourseGroupDivs(self, soup):
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

    def getCourseSectionDivs(self, groupDivTag):
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

    def isCancelled(self, sectionTag):
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
        
    def getDetailsDiv(self, sectionTag):
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

    def getMeetingInfoDivs(self, sectionDetailsTag):
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

    def getSectionMeetingInfo(self, meetingInfoDiv, semProfDict):
        """
        This function extracts specific info from a meeting info div.
        There are two cases.
        1.) The meeting info has five divs, and includes the days and times.
        - [0] (first div) is Days the class meets, e.g. MWF
        - [1] (second div) is Times the class meets, e.g. 10:00 AM - 10:50 AM
        - [2] (third div) is session period, e.g. 9/2/2009 - 12/15/2009
        - [3] (fourth div) is Instructor
        - [4] (fifth div) is Room Number
        2.) The meeting info has five divs, but two have no info in them.
        - [0] is Days the class meets, but is empty in this case
        - [1] is Times the class meets, but is empty in this case
        - [2] is session period, e.g. 9/2/2009 - 12/15/2009
        - [3] is Instructor
        - [4] is Room Number
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
        try:
            days = daySpans[3].getText()
            if len(days) == 0:
                days = "Unknown"
        except:
            days = "Unknown"

        # Get the times
        timeSpans = timesCell.find_all('span')
        try:
            timeStart = timeSpans[1].getText()
            timeEnd = timeSpans[3].getText()
        except:
            timeStart = "Unknown"
            timeEnd = "Unknown"

        # Get the session
        sessionSpans = sessionCell.find_all('span')
        try:
            sessionStart = sessionSpans[1].getText()
            sessionEnd = sessionSpans[2].getText()
            sessionEnd = sessionEnd.replace(' ', '').replace('–', '')
        except:
            sessionStart = "Unknown"
            sessionEnd = "Unknown"

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

    def getQuickInfoDetails(self, sectionDetailsTag):
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
        if len(textSectionDivs) < 3:
            quickInfoDiv = textSectionDivs[1]
        else:
            quickInfoDiv = textSectionDivs[2]
        usersIcon = quickInfoDiv.find("i", attrs = {'class': 'fa-users'})

        # Note that this only matters if we had an enrollment requirements section
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
        if ')' in creditValue:
            creditValue = creditsSpans[2].getText()

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

    def getProfTotalsDict(self, semesterProfs):
        """
        This function gets the total number of sections every professor
        instructed for a course for all the semesters requested.

        Parameters
        ----------
        semesterProfs : list
            A list where each element is a list of two elements:
            - [0] is the course term as a human readable string
            - [1] is the dict with every professor for that semester

        Returns
        -------
        dict
            The dictionary that has professor names as keys, and their
            total section count as an int value.
        """
        profTotals = {}
        for sem in semesterProfs:
            semDict = sem[1]
            for prof in semDict:
                if prof not in profTotals:
                    profTotals[prof] = semDict[prof]
                else:
                    profTotals[prof] += semDict[prof]
        return profTotals

    def combineInfoDicts(self, qInfoDict, meetInfoDicts, sem):
        """
        This function combines both the quick info and meeting info
        dictionaries for one course section into one dictionary.

        Parameters
        ----------
        qInfoDict : dict
            The dictionary with the quick info for the class section.
        meetInfoDicts : list
            The list of dictionaries with the meeting info for the
            class section. Usually this is just 1, but in some cases
            it can be 2.
        sem : str
            The semester as a human-readable string.

        Returns
        -------
        dict
            The dictionary that has the quick info and all meeting
            sections for one course section in the semester.
        """

        # First start with the quick info
        combineDict = {}
        combineDict['enrollNow'] = qInfoDict['enrollNow']
        combineDict['enrollMax'] = qInfoDict['enrollMax']
        combineDict['creditValue'] = qInfoDict['creditValue']
        combineDict['honors'] = qInfoDict['honors']
        combineDict['semester'] = sem

        # Now add the meeting info for this course section.
        combineDict['meetings'] = []
        for meetDict in meetInfoDicts:
            combineDict['meetings'].append(meetDict)
        return combineDict


    ####################################
    # PRINTING (FOR DEBUGGING)         #
    ####################################

    def printMeetingInfoDict(self, meetInfoDict):
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

    def printQuickInfoDict(self, qInfoDict):
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


    ####################################
    # WRITING TO AN OPEN FILE          #
    ####################################

    def writeStringToFile(self, openFile, string):
        """
        This function writes out the passed string to a passed file that
        is currently open in write mode.

        Parameters
        ----------
        openFile : _io.TextIOWrapper
            A file that is already open in write mode, and we will write
            to this file.
        str : string
            The string to write out to the open file. Note that the proper
            formatting should already be included e.g. newlines.
        """
        openFile.write(string)

    def writeQuickInfoToFile(self, openFile, qInfoDict):
        """
        This function writes out the passed Quick Info dictionary to a
        passed file that is currently open in write mode.

        Parameters
        ----------
        openFile : _io.TextIOWrapper
            A file that is already open in write mode, and we will write
            to this file.
        qInfoDict : dict
            The dictionary with the quick info for the class section.
        """
        if qInfoDict is None:
            openFile.write("> No enrollment, credit, or honors info found.\n")
        else:
            openFile.write("> Enrolled Now:   " + qInfoDict['enrollNow'] + "\n")
            openFile.write("> Enrollment Max: " + qInfoDict['enrollMax'] + "\n")
            openFile.write("> Credit Value:   " + qInfoDict['creditValue'] + "\n")
            openFile.write("> Honors Section: " + qInfoDict['honors'] + "\n")

    def writeMeetingInfoToFile(self, openFile, meetInfoDict):
        """
        This function writes out the passed Meeting Info dictionary to a
        passed file that is currently open in write mode.

        Parameters
        ----------
        openFile : _io.TextIOWrapper
            A file that is already open in write mode, and we will write
            to this file.
        meetInfoDict : dict
            The dictionary with the meeting info for the class section.
        """
        if meetInfoDict is None:
            openFile.write("> No meeting info found.\n")
        else:
            openFile.write("> Meeting Days:   " + meetInfoDict['days'] + "\n")
            openFile.write("> Time Start:     " + meetInfoDict['timeStart'] + "\n")
            openFile.write("> Time End:       " + meetInfoDict['timeEnd'] + "\n")
            openFile.write("> Session Start:  " + meetInfoDict['sessionStart'] + "\n")
            openFile.write("> Session End:    " + meetInfoDict['sessionEnd'] + "\n")
            openFile.write("> Instructor:     " + meetInfoDict['instructor'] + "\n")
            openFile.write("> Room:           " + meetInfoDict['room'] + "\n")

    

    def writeSemCountsToFile(self, openFile):
        """
        This function writes out the professor individual section
        count for every semester.

        Parameters
        ----------
        openFile : _io.TextIOWrapper
            A file that is already open in write mode, and we will write
            to this file.
        """
        for sem in self.semesterProfs:
            string = ">> Writing professor count for semester " + sem[0] + "\n"
            self.writeStringToFile(openFile, string)
            semDict = sem[1]
            for prof in sorted(semDict):
                string = "> " + prof + ": " + str(semDict[prof]) + "\n"
                self.writeStringToFile(openFile, string)

    def writeProfTotals(self, openFile):
        """
        This function writes out the total sections for each professor
        across the range of semesters specified.

        Parameters
        ----------
        openFile : _io.TextIOWrapper
            A file that is already open in write mode, and we will write
            to this file.
        """
        for prof in self.profTotals:
            string = "> " + prof + ": " + str(self.profTotals[prof]) + "\n"
            self.writeStringToFile(openFile, string)

# End
