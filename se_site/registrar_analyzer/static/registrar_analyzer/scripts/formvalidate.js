/*****************************************************
 *
 * File:          formvalidate.js
 * Authors:       Roy Van Liew
 * Description:   Javascript file which provides
 *                a check for the start and end
 *                semester in the /ra form.
 *
 ****************************************************/

// termDict is a dictionary that houses the semester term for the URL
// This will be used to compare the semester range
var termDict = new Object();
termDict['Fall 2000'] = '1010';
termDict['Spring 2001'] = '1030';
termDict['Fall 2001'] = '1110';
termDict['Spring 2002'] = '1130';
termDict['Fall 2002'] = '1210';
termDict['Spring 2003'] = '1230';
termDict['Fall 2003'] = '1310';
termDict['Spring 2004'] = '1330';
termDict['Fall 2004'] = '1410';
termDict['Spring 2005'] = '1430';
termDict['Fall 2005'] = '1510';
termDict['Spring 2006'] = '1530';
termDict['Fall 2006'] = '1610';
termDict['Spring 2007'] = '1630';
termDict['Fall 2007'] = '1710';
termDict['Spring 2008'] = '1730';
termDict['Fall 2008'] = '1810';
termDict['Spring 2009'] = '1830';
termDict['Fall 2009'] = '1910';
termDict['Spring 2010'] = '1930';
termDict['Fall 2010'] = '2010';
termDict['Spring 2011'] = '2030';
termDict['Fall 2011'] = '2110';
termDict['Spring 2012'] = '2130';
termDict['Fall 2012'] = '2210';
termDict['Spring 2013'] = '2230';
termDict['Fall 2013'] = '2310';
termDict['Spring 2014'] = '2330';
termDict['Fall 2014'] = '2410';
termDict['Spring 2015'] = '2430';
termDict['Fall 2015'] = '2510';
termDict['Spring 2016'] = '2530';
termDict['Fall 2016'] = '2610';
termDict['Spring 2017'] = '2630';

/* This is for checking if the start semester is before or on the end semester. */
function validStartAndEndSemester() {

    // First access our selects from the form and get their selected values
    var startSemesterSelect = $('#startSemesterSelect');
    var endSemesterSelect = $('#endSemesterSelect');
    var startSemester = startSemesterSelect.val();
    var endSemester = endSemesterSelect.val();

    // Now use termDict to convert the selected semester string into a number string
    var startStr = termDict[startSemester];
    var endStr = termDict[endSemester];
    var startNum = parseInt(startStr);
    var endNum = parseInt(endStr);

    // Now we can compare the semester values. Only submit if start semester is <= the end semester
    if (startNum > endNum) {
        var alertText = '<div id="badInput" class="alert alert-danger"> \
<a href="#" class="close" data-dismiss="alert" \
aria-label="close"> &times;</a> \
<strong>The Start Semester cannot be after the End Semester.</strong></div>';
        $('div#semesterError').html(alertText);
        return false;
    } else {
        document.graphForm.submit();
    }

}