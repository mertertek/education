from django.shortcuts import render
from .models import CustomUser, Instructor, Student
from course.models import Certificate
from course.serializers import CertificateSerializer
from .serializers import CustomUserSerializer, InstructorSerializer, StudentSerializer, UserRegisterationSerializer, UserLoginSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access":str(token.access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            user_serializer = CustomUserSerializer(user)
            token = RefreshToken.for_user(user)
            data = user_serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstructorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instructors = Instructor.objects.all()
        serializer = InstructorSerializer(instructors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstructorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        instructor = get_object_or_404(Instructor, pk=pk)
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        instructor = get_object_or_404(Instructor, pk=pk)
        serializer = InstructorSerializer(instructor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instructor = get_object_or_404(Instructor, pk=pk)
        if request.user.is_staff:
            instructor.delete()
            return Response({"message":"Instructor deleted"},status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"You have not permission detele this instructor"},status=status.HTTP_204_NO_CONTENT)

class StudentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        certificates = Certificate.objects.filter(course_user=student)
        student_serializer = StudentSerializer(student)
        certificate_serializer = CertificateSerializer(certificates, many=True)
        
        return Response({"student": student_serializer.data, "certificates": certificate_serializer.data}, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        if request.user.is_staff:
            student.delete()
            return Response({"message":"Student deleted"},status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"You have not permission detele this student"},status=status.HTTP_204_NO_CONTENT)
