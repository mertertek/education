from rest_framework import serializers
from .models import Course, Certificate, StudentProgress, CourseText
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"

class StudentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgress
        fields = "__all__"

class CourseTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseText
        fields = "__all__"
