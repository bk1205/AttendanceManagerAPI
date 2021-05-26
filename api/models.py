from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

attStatus = (
    ('present', 'Present'), ('absent', 'Absent'), ('leave', 'Leave')
)

class Class(models.Model):
    cId = models.IntegerField(default=1, validators=[MaxValueValidator(12), MinValueValidator(1)],
                               primary_key=True)
    # instructer = models.CharField(max_length=50)
    def __str__(self):
        return str(self.cId)


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    rollNo = models.IntegerField()
    name = models.CharField(max_length=50)
    cId = models.ForeignKey(to=Class, null=True, blank=True, on_delete=models.CASCADE,)
    # city = models.CharField(max_length=100)

    class Meta:
        unique_together = ('rollNo', 'cId',)
        db_table = 'students'

    def __str__(self):
        return self.name


class Attendance(models.Model):
    attStatus = (
        ('present', 'Present'), ('absent', 'Absent'), ('leave', 'Leave')
    )
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, related_name='attendance')
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







