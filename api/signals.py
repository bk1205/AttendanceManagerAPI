from api.models import Attendance, Student
from django.db.models.signals import post_save
from django.dispatch import receiver

attStatus = (
    ('present', 'Present'), ('absent', 'Absent'), ('leave', 'Leave')
)

@receiver(post_save, sender=Student, dispatch_uid="create_attendance_object")
def create_attendance_object(sender, instance, created, update_fields, **kwargs):
    if created:
        obj = Attendance.objects.create(student=instance, status='present')
        obj.save()
        print('Attendance object created')

