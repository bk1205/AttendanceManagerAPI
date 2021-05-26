from django.urls import path

from api.views import UserRecordView, StudentAPI, AttendanceAPI, ReportView

urlpatterns = [
    path('students/', StudentAPI.as_view()),
    path('students/<int:pk>/', StudentAPI.as_view()),
    path('students/cid/<int:cId>/', StudentAPI.as_view()),
    path('attendance/<int:cId>/', AttendanceAPI.as_view()),
    path('attendance/update/<int:cId>/', AttendanceAPI.as_view()),
    path('reports/<int:cId>/<str:dates>', ReportView.as_view()),
    path('user/', UserRecordView.as_view(), name='users'),

]
