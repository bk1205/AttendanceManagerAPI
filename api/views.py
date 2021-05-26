import io
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
import csv
from datetime import datetime
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.response import Response
from rest_framework import status
from  django.utils.dateparse import parse_date
from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Student, Attendance
from api.serializers import StudentModelSerializer, UserSerializer, AttendanceSerializer, AttendanceListSerializer


class StudentAPI(APIView):

    def get(self, request, pk=None, cId=None):
        id = pk
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentModelSerializer(stu)
            return Response(serializer.data)
        if cId is not None:
            students = Student.objects.filter(cId=cId)
            serializer = StudentModelSerializer(students, many=True)
            return Response(serializer.data)
        stu = Student.objects.all()
        serializer = StudentModelSerializer(stu, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        serializer = StudentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def put(self, request, pk=None):
        id = pk
        stu = Student.objects.get(pk=id)
        serializer = StudentModelSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data updated'})
        return Response(serializer.errors)

    def patch(self, request, pk):
        id = pk
        stu = Student.objects.get(pk=id)
        serializer = StudentModelSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data updated'})
        return Response(serializer.errors)

    def delete(self, request, pk):
        id = pk
        stu = Student.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})


class AttendanceAPI(APIView):
    def get(self, request, cId):
        attendances = Attendance.objects.filter(student__cId=cId)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    def post(self, request, cId):
        students = Student.objects.filter(cId=cId)
        print(request.data)
        date = parse_date(request.data['date'])
        print(date)
        attendances = []
        for stu in students:
            att = Attendance.objects.get_or_create(student=stu, attendance_date=date)
            print(att)
            serializer = AttendanceSerializer(att[0])
            print(serializer.data)
            attendances.append(serializer.data)
        return Response(attendances)

    def patch(self, request, cId):
        print(request.data)
        attendances = Attendance.objects.filter(student__cId=cId)
        print(attendances)
        dateStr = [request.data[0]['attendance_date']]
        print(dateStr)
        data = {
            a['id']: {k: v for k, v in a.items() if k != 'id'}
            for a in request.data
        }
        data_list = data.keys()
        print(data_list)
        print([x.student.id for x in attendances])
        attendances_final = [x for x in attendances if x.student.id in data_list]
        attendances_final1 = [x for x in attendances_final if str(x.attendance_date) in dateStr]
        print(attendances_final1)
        print(data)
        for inst in attendances_final1:
            serializer = AttendanceSerializer(inst, data=data[inst.student.id], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({})

    # def patch(self, request, cId):
    #     # students = Student.objects.filter(cId=cId)
    #     # # print(students)
    #     # attendances = [student.attendance.all() for student in students]
    #
    #     attendances = Attendance.objects.filter(student__cId=cId)
    #     print(attendances)
    #     # print(list(attendances[0]))
    #     # attendances = [list(att) for att in attendances]
    #     # print(attendances)
    #     # print(request.data)
    #     serializer = AttendanceSerializer(attendances, data=request.data, partial=True, many=True)
    #     # print(serializer.initial_data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'msg': 'Complete Data updated'})
    #     return Response(serializer.errors,status=status.HTTP_200_OK)

    def put(self, request, pk):
        id = pk
        att = Attendance.objects.get(pk=id)
        serializer = AttendanceSerializer(att, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data updated'})
        return Response(serializer.errors)


class ReportView(APIView):
    def get(self, request, cId, dates):
        print(cId)
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        fromDate, toDate = dates.split('+')
        # totalDays = (datetime.strptime(fromDate, "%Y-%m-%d") - datetime.strptime(toDate, "%Y-%m-%d")).days
        daterange = pd.date_range(fromDate, toDate, )
        print(daterange)
        fieldNames = ['ID', 'STUDENT NAME']
        for i in daterange:
            day = i.strftime('%Y-%m-%d')
            print(day)
            fieldNames.append(day)
        print(fieldNames)
        writer = csv.DictWriter(response, fieldnames=fieldNames)
        writer.writeheader()
        data = Attendance.objects.filter(student__cId=cId)
        stuName = []
        for row in data:
            if row.student.name not in stuName:
                stuName.append(row.student.name)
        print(len(stuName))
        for name, row in zip(stuName, data):
            filtered = data.filter(student__name=name).values()
            print(filtered)
            rowDict = {
                'STUDENT NAME': name,
            }
            for qs in filtered:
                if(str(qs['attendance_date']) not in fieldNames):
                    continue
                dateStr = str(qs['attendance_date'])
                rowDict['ID'] = qs['student_id']
                rowDict[f'{dateStr}'] = qs['status']
                print(dateStr)
            print(rowDict)
            writer.writerow(rowDict)

        reader = csv.DictReader(io.TextIOWrapper(io.BytesIO(response.content), encoding='utf-8'))
        for row in reader:
            print(row)

        return response






class UserRecordView(APIView):
    '''API View to create or get a list of all the registered users. GET request returns the registered users whereas a POST request allows to create a new user'''
    # permission_classes = [IsAdminUser]
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)































#
# def student_details(request, id):
#     stu = Student.objects.get(id=id)
#     serializer = StudentModelSerializer(stu)
#     json_data = JSONRenderer().render(serializer.data)
#     return HttpResponse(json_data, content_type='application/json')
#
# def students(request):
#     stu = Student.objects.all()
#     serializer = StudentModelSerializer(stu, many=True)
#     # json_data = JSONRenderer().render(serializer.data,)
#     # return HttpResponse(json_data, content_type='application/json')
#     return JsonResponse(serializer.data, safe=False)
#
#
# @csrf_exempt
# def student_create(request):
#     if request.method == 'POST':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         serializer = StudentModelSerializer(data=pythondata)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg': 'Data created'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type='application/json')
#         return JsonResponse(serializer.errors, safe=False)


#Here we are using  API views provided by DRF which will do the most of the work (rendering, parsing etc.) for us and
# we can get the functionality by less code.
'''@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@authentication_classes([BaseAuthentication])
@permission_classes([IsAuthenticated])
def student_api(request, pk=None):
    if request.method == 'GET':
        # id = request.data.get('id')
        id = pk
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentModelSerializer(stu)
            return Response(serializer.data)
        stu = Student.objects.all()
        serializer = StudentModelSerializer(stu, many=True)
        return Response(serializer.data)


    if request.method == 'POST':
        serializer = StudentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data created'},  status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


    if request.method == 'PUT':
        # id = request.data.get('id')
        id = pk
        stu = Student.objects.get(pk=id)
        serializer = StudentModelSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data updated'})
        return Response(serializer.errors)

    if request.method == 'PATCH':
        # id = request.data.get('id')
        id = pk
        stu = Student.objects.get(pk=id)
        serializer = StudentModelSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data updated'})
        return Response(serializer.errors)


    if request.method == 'DELETE':
        # id = request.data.get('id')
        id = pk
        stu = Student.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'})'''



