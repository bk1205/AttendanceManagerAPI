from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

attStatus = (
    ('present', 'Present'), ('absent', 'Absent'), ('leave', 'Leave')
)

class Class(models.Model): #A TABLE WITH 1 FIELDS/COLUMN AS DEFINED BELOW
    cId = models.IntegerField(default=1, validators=[MaxValueValidator(12), MinValueValidator(1)],
                               primary_key=True)
    # instructer = models.CharField(max_length=50)
    def __str__(self):
        return str(self.cId)


class Student(models.Model): #A TABLE WITH 4 FIELDS AS DEFINED BELOW
    id = models.AutoField(primary_key=True)
    rollNo = models.IntegerField()
    name = models.CharField(max_length=50)
    cId = models.ForeignKey(to=Class, null=True, blank=True, on_delete=models.CASCADE,)
    # city = models.CharField(max_length=100)

    class Meta:
        unique_together = ('rollNo', 'cId',) #Roll No of two students in same class cannot be same and similarly
        # class of two students with same roll no cannot be same
        db_table = 'students'

    def __str__(self):
        return self.name


class Attendance(models.Model): #A TABLE WITH 5 FIELDS AS DEFINED BELOW
    attStatus = (
        ('present', 'Present'), ('absent', 'Absent'), ('leave', 'Leave')
    )
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, related_name='attendance') #ManytoOne Relation
    attendance_date = models.DateField(default=datetime.now())
    status = models.CharField(choices=attStatus, max_length=10, null=True, blank=True)
    #
    # class Meta:
    #     unique_together = ('student', 'attendance_date')

    def save(self, *args, **kwargs):
        print('hi')
        if not self.status:
            self.status = attStatus[0][0]
        print(self.status)
        super(Attendance, self).save(*args, **kwargs)







