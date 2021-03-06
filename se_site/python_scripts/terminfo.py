##################################
# DICTIONARIES FOR SEMESTER INFO #
##################################

# termDict is a dictionary that houses the semester term for the URL
termDict = {}
termDict['Fall 2000'] = '1010'
termDict['Spring 2001'] = '1030'
termDict['Fall 2001'] = '1110'
termDict['Spring 2002'] = '1130'
termDict['Fall 2002'] = '1210'
termDict['Spring 2003'] = '1230'
termDict['Fall 2003'] = '1310'
termDict['Spring 2004'] = '1330'
termDict['Fall 2004'] = '1410'
termDict['Spring 2005'] = '1430'
termDict['Fall 2005'] = '1510'
termDict['Spring 2006'] = '1530'
termDict['Fall 2006'] = '1610'
termDict['Spring 2007'] = '1630'
termDict['Fall 2007'] = '1710'
termDict['Spring 2008'] = '1730'
termDict['Fall 2008'] = '1810'
termDict['Spring 2009'] = '1830'
termDict['Fall 2009'] = '1910'
termDict['Spring 2010'] = '1930'
termDict['Fall 2010'] = '2010'
termDict['Spring 2011'] = '2030'
termDict['Fall 2011'] = '2110'
termDict['Spring 2012'] = '2130'
termDict['Fall 2012'] = '2210'
termDict['Spring 2013'] = '2230'
termDict['Fall 2013'] = '2310'
termDict['Spring 2014'] = '2330'
termDict['Fall 2014'] = '2410'
termDict['Spring 2015'] = '2430'
termDict['Fall 2015'] = '2510'
termDict['Spring 2016'] = '2530'
termDict['Fall 2016'] = '2610'
termDict['Spring 2017'] = '2630'

# All semesters
allSemesters = ['1010', '1030', '1110', '1130', '1210', '1230', '1310', '1330', '1410', '1430', '1510', '1530', '1610', '1630', '1710', '1730', '1810', '1830', '1910', '1930', '2010', '2030', '2110', '2130', '2210', '2230', '2310', '2330', '2410', '2430', '2510', '2530', '2610', '2630']
allFallSemesters = ['1010', '1110', '1210', '1310', '1410', '1510', '1610', '1710', '1810', '1910', '2010', '2110', '2210', '2310', '2410', '2510', '2610']
allSpringSemesters = ['1030', '1130', '1230', '1330', '1430', '1530', '1630', '1730', '1830', '1930', '2030', '2130', '2230', '2330', '2430', '2530', '2630']

# Going from term number to term instead
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

# courseDict is a dictionary that translates the input course into the url course.
courseDict = {}

# Mandatory courses
courseDict['algorithms'] = 'Analysis%20of%20Algorithms%20(Formerly%209'
courseDict['assembly'] = 'Assembly%20Language%20Programming%20(Formerly%2091.203)'
courseDict['arch'] = 'Computer%20Architecture%20(Formerly%2091.305)'
courseDict['cp1'] = 'Computing%20I%20(Formerly%2091.101)'
courseDict['cp2'] = 'Computing%20II%20(Formerly%2091.102)'
courseDict['cp3'] = 'Computing%20III%20(Formerly%2091.201)'
courseDict['cp4'] = 'Computing%20IV%20(Formerly%2091.204)'
courseDict['foundations'] = 'Foundations%20of%20Computer%20Science%20(Formerly%2091.304)'
courseDict['os'] = 'Operating%20Systems%20(Formerly%2091.308)'
courseDict['opl'] = 'Organization%20of%20Programming%20Languages%20(Formerly%2091.301)'

# Electives
courseDict['ai'] = 'Artificial%20Intelligence%20(Formerly%2091.420)'
courseDict['compiler'] = 'Compiler%20Construction%20I%20(Formerly%2091.406)'
courseDict['cg2'] = '(Formerly%2091.428)'
courseDict['cg1'] = 'Computer%20Graphics%20I%20(Formerly%2091.427)'
courseDict['cv'] = 'Computer%20Vision%20I%20(Formerly%2091.423'
courseDict['cybercrime'] = 'Cyber%20Crime%20Investigation'
courseDict['dc1'] = 'Data%20Communications%20I%20(Formerly%2091.413)'
courseDict['dc2'] = 'Data%20Communications%20II%20(Formerly%2091.414)'
courseDict['datamining'] = 'Data%20Mining%20(Formerly%2091.421)'
courseDict['db1'] = 'Database%20I%20(Formerly%2091.309)'
courseDict['db2'] = 'Database%20II%20(Formerly%2091.310)'
courseDict['gui1'] = 'Graphical%20User%20Interface%20Programming%20I%20(Formerly%2091.461)'
courseDict['gui2'] = 'Graphical%20User%20Interface%20Programming%20II%20(Formerly%2091.462)'
courseDict['ml'] = 'Machine%20Learning%20(Formerly%2091.422)'
courseDict['mobileapp2'] = 'Mobile%20App%20Programming%20ll'
courseDict['mobilerobotics1'] = 'Mobile%20Robotics%20I%20(Formerly%2091.450)'
courseDict['mobilerobotics2'] = 'Mobile%20Robotics%20II%20(Formerly%2091.451)'
courseDict['nlp'] = 'Natural%20Language%20Processing%20(Formerly%2091.442'
courseDict['selected'] = 'Selected%20Topics%20(Formerly%2091.460)'
courseDict['se1'] = 'Software%20Engineering%20I%20(Formerly%2091.411)'
courseDict['se2'] = 'Software%20Engineering%20II%20(Formerly%2091.412)'
courseDict['special'] = 'Special%20Topics%20(Formerly%2091.350)'


# This dictionary is used to get human-readable translation for a course.
courseNameDict = {}

# Mandatory courses
courseNameDict['cp1'] = 'Computing I'
courseNameDict['cp2'] = 'Computing II'
courseNameDict['cp3'] = 'Computing III'
courseNameDict['cp4'] = 'Computing IV'
courseNameDict['assembly'] = 'Assembly Language Programming'
courseNameDict['opl'] = 'Organization of Programming Languages'
courseNameDict['foundations'] = 'Foundations of Computer Science'
courseNameDict['arch'] = 'Computer Architecture'
courseNameDict['os'] = 'Operating Systems'
courseNameDict['algorithms'] = 'Analysis of Algorithms'

# Electives
courseNameDict['ai'] = 'Artificial Intelligence'
courseNameDict['compiler'] = 'Compiler Construction I'
courseNameDict['cg2'] = 'Computer Graphics'
courseNameDict['cg1'] = 'Computer Graphics I'
courseNameDict['cv'] = 'Computer Vision I'
courseNameDict['cybercrime'] = 'Cyber Crime Investigation'
courseNameDict['dc1'] = 'Data Communications I'
courseNameDict['dc2'] = 'Data Communications II'
courseNameDict['datamining'] = 'Data Mining'
courseNameDict['db1'] = 'Database I'
courseNameDict['db2'] = 'Database II'
courseNameDict['gui1'] = 'Graphical User Interface Programming I'
courseNameDict['gui2'] = 'Graphical User Interface Programming II'
courseNameDict['ml'] = 'Machine Learning'
courseNameDict['mobileapp2'] = 'Mobile App Programming ll'
courseNameDict['mobilerobotics1'] = 'Mobile Robotics I'
courseNameDict['mobilerobotics2'] = 'Mobile Robotics II'
courseNameDict['nlp'] = 'Natural Language Processing'
courseNameDict['selected'] = 'Selected Topics'
courseNameDict['se1'] = 'Software Engineering I'
courseNameDict['se2'] = 'Software Engineering II'
courseNameDict['special'] = 'Special Topics'

# List of course names in sorted order
sortedFullCourseNames = ['Analysis of Algorithms', 'Artificial Intelligence', 'Assembly Language Programming', 'Compiler Construction I', 'Computer Architecture', 'Computer Graphics', 'Computer Graphics I', 'Computer Vision I', 'Computing I', 'Computing II', 'Computing III', 'Computing IV', 'Cyber Crime Investigation', 'Data Communications I', 'Data Communications II', 'Data Mining', 'Database I', 'Database II', 'Foundations of Computer Science', 'Graphical User Interface Programming I', 'Graphical User Interface Programming II', 'Machine Learning', 'Mobile App Programming ll', 'Mobile Robotics I', 'Mobile Robotics II', 'Natural Language Processing', 'Operating Systems', 'Organization of Programming Languages', 'Selected Topics', 'Software Engineering I', 'Software Engineering II', 'Special Topics']

# List of semester range in order
orderedSemesterList = ['Fall 2000', 'Spring 2001', 'Fall 2001', 'Spring 2002', 'Fall 2002', 'Spring 2003', 'Fall 2003', 'Spring 2004', 'Fall 2004', 'Spring 2005', 'Fall 2005', 'Spring 2006', 'Fall 2006', 'Spring 2007', 'Fall 2007', 'Spring 2008', 'Fall 2008', 'Spring 2009', 'Fall 2009', 'Spring 2010', 'Fall 2010', 'Spring 2011', 'Fall 2011', 'Spring 2012', 'Fall 2012', 'Spring 2013', 'Fall 2013', 'Spring 2014', 'Fall 2014', 'Spring 2015', 'Fall 2015', 'Spring 2016', 'Fall 2016', 'Spring 2017']



# End