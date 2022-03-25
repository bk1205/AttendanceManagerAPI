from django.contrib import admin

# Register your models here.
from api.models import Student, Class, Attendance

# The admin.py file is used to display your models in the Django admin panel. You can also customize your admin panel.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'rollNo', 'name', 'cId']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['cId']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'cId', 'attendance_date', 'status']
    def id(self, obj):
        return obj.student.id
    def cId(self, obj):
        return obj.student.cId
    id.admin_order_field = 'student'
    cId.admin_order_field = 'student'