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
    semester = models.DateField('semester_offered')
    time_start = models.DateTimeField('time_start')
    course_title = models.CharField(max_length=200)
    enroll_now = models.IntegerField()
    enroll_max = models.IntegerField()
    honors = models.BooleanField()
    credit_value = models.IntegerField()
    meeting_days = models.CharField(max_length=10)
    instructor = models.CharField(max_length=200)

    # constrant for the index
    class Meta:
        index_together = ("semester", "time_start", "course_title", "instructor", "meeting_days")


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
class ClassTotals(models.Model):
    course = models.CharField(max_length=200)
    professor_total = models.IntegerField()

    class Meta:
        unique_together = ("course", "professor_total")
