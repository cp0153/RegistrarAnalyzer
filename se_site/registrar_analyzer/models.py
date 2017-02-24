from django.db import models
# django by default has an autoincrement primary key, I think it should be one row per section
# One table for each course, where every row will have the following columns:
#  Semester
#  CourseTitle
#  EnrollNow
#  EnrollMax
#  Honors
#  CreditValue
#  Meeting_days
#  Instructor1


# Create your models here.
class Courses(models.Model):
    course_name = models.CharField(max_length=200)
    semester = models.CharField(max_length=200,)
    time_start = models.CharField(max_length=200)
    time_end = models.CharField(max_length=200)
    enroll_now = models.IntegerField()
    enroll_max = models.IntegerField()
    honors = models.CharField(max_length=200)
    credit_value = models.IntegerField()
    meeting_days = models.CharField(max_length=10)
    instructor = models.CharField(max_length=200)
    room = models.CharField(max_length=200)

    # constrant for the index
    class Meta:
        unique_together = ("course_name", "semester", "time_start", "time_end", "enroll_now", "enroll_now",
                           "honors", "room", "instructor", "meeting_days", "enroll_now")


# >>> Writing Professor Totals for Computing IV for semesters Fall 2000 through Spring 2017
# > Li Xu: 8
# > Xinwen Fu: 8
# > Gary Livingston: 1
# > Yelena Rykalova: 3
# > Fred Martin: 2
# > TBA: 2
# > Jesse Heines: 5
# > William Moloney Jr: 3
# > Robert Lechner: 2
# > Marc Chiarini: 2
# > Ayat Hatem: 2
# > Victor Grinberg: 1
# > John Sieg Jr: 11

# no longer needed
# class ClassTotals(models.Model):
#     course_name = models.CharField(max_length=200)
#     prof_total = models.IntegerField()
#     semester = models.CharField(max_length=200)
#
#     class Meta:
#         unique_together = ("course_name", "prof_total")

# a = [{'creditValue': '4 Credits', 'course': 'Computing I', 'enrollNow': '50', 'honors': 'No',
#       'enrollMax': '60', 'semester': 'Fall 2005', 'meetings':
#           [{'sessionEnd': '12/22/2005', 'instructor': 'James Canning', 'days': 'MWRF',
#             'sessionStart': '9/6/2005', 'timeEnd': '11:20 AM', 'timeStart': '10:30 AM',
#             'room': 'OS 408'}]},
#      {'creditValue': '4 Credits', 'course': 'Computing I', 'enrollNow': '7', 'honors': 'Yes',
#       'enrollMax': '25', 'semester': 'Fall 2005', 'meetings':
#           [{'sessionEnd': '12/22/2005', 'instructor': 'James Canning', 'days': 'MWRF',
#             'sessionStart': '9/6/2005', 'timeEnd': '11:20 AM',
#             'timeStart': '10:30 AM', 'room': 'OS 408'}]}]
#
# b = {'creditValue': '4 Credits', 'course': 'Computing I', 'enrollNow': '7', 'honors': 'Yes',
#      'enrollMax': '25', 'semester': 'Fall 2005', 'meetings':
#          [{'sessionEnd': '12/22/2005', 'instructor': 'James Canning', 'days': 'MWRF',
#            'sessionStart': '9/6/2005', 'timeEnd': '11:20 AM', 'timeStart': '10:30 AM',
#            'room': 'OS 408'}]}

# reset migrations on development database
# type the following into the cmd line:
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc"  -delete

# then delete db.sqlite3
# finally, create the initial migrations and generate schema
# python manage.py makemigrations
# python manage.py migrate
