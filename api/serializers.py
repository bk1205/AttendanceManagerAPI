from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from api.models import Student, Class, Attendance


def starts_with_r(value):
    if value[0].lower() != 'r':
        raise serializers.ValidationError('Name should be start with R')


# class StudentSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=50, validators=[starts_with_r])
#     rollNo = serializers.IntegerField()
#     city = serializers.CharField(max_length=100)
#
#     #field_level validation
#     def validate_rollNo(self, value):
#         if value >= 8000:
#             raise serializers.ValidationError('Seats full')
#         return value
#
#     #object_level validation
#     def validate(self, data):
#         name = data.get('name')
#         city = data.get('city')
#         if name.lower() == 'rohit' and city.lower() == 'jodhpur':
#             raise serializers.ValidationError('City must be other than Jodhpur!')
#         return data
#
#     def create(self, validated_data):
#         return Student.objects.create(**validated_data)

class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['rollNo', 'name', 'cId']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['cId']

class AttendanceListSerializer(serializers.ListSerializer):
    def update(self, instances, validated_data):
        print(instances)
        instance_hash = {instance.id: instance for instance in instances}
        print(instance_hash)
        # print(validated_data)
        result = [self.child.update(instance_hash[index], attrs) for index, attrs in enumerate(validated_data)]
        # print(result)
        # for attr, value in result:
        #     print(attr)
        #     print(value)
        #print(validated_data)
        return result

    class Meta:
        model = Attendance
        fields = ['student_name', 'attendance_date', 'status']

class AttendanceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='student.id')
    print('hello')
    # print(id)
    student_name = serializers.CharField(source='student.name', read_only=True,)
    status = serializers.CharField()
    attendance_date = serializers.DateField()

    class Meta:
        model = Attendance
        fields = ['id', 'student_name', 'attendance_date', 'status']
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Attendance.objects.all(),
        #         fields=['student_id', 'attendance_date']
        #     )
        # ]
        # list_serializer_class = AttendanceListSerializer



class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    class Meta:
        model = User
        fields = (
            'username',
            # 'first_name',
            # 'last_name',
            # 'email',
            'password',
        )
        validators = [
            #If both username and email are same then the below validator will mark the data invalid!
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', ]
            )
        ]