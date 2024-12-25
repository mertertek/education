from django.shortcuts import render
from .models import Course , CourseText, StudentProgress, Certificate
from user.models import Instructor, Student
from .serializers import CourseSerializer, CourseTextSerializer, StudentProgressSerializer, CourseTextSerializer
from user.serializers import InstructorSerializer, StudentSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if course.instructor.user != request.user and not request.user.is_staff:
            return Response({"error": "You do not have permission to edit this course."}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if course.instructor.user != request.user and not request.user.is_staff:
            course.delete()
        else:
            return Response({"error": "You do not have permission to delete this course."}, status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)

class JoinCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        student = get_object_or_404(Student, user=request.user)
        course = get_object_or_404(Course, pk=course_id)

        if course.students.filter(id=student.id).exists():
            return Response({"message": "You are already enrolled in this course."}, status=status.HTTP_200_OK)

        course.students.add(student)
        course.save()
        return Response({"message": "Successfully joined the course."}, status=status.HTTP_200_OK)

class CourseTextAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        student = get_object_or_404(Student, user=request.user)
        course = get_object_or_404(Course, id=course_id)

        if not course.students.filter(id=student.id).exists():
            return Response({"error": "You are not joined this course."}, status=status.HTTP_403_FORBIDDEN)

        texts = course.texts.all()
        serializer = CourseTextSerializer(texts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        if course.instructor.user != request.user:
            return Response({"error": "Only the instructor can add texts."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseTextSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            course.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkTextAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, text_id, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        course_text = get_object_or_404(CourseText, id=text_id)
        course = course_text.course

        if not course.students.filter(id=student.id).exists():
            return Response({"error": "You have not joined this course."}, status=status.HTTP_403_FORBIDDEN)

        progress, created = StudentProgress.objects.get_or_create(student=student, course_text=course_text)

        if not progress.is_read:
            progress.is_read = True
            progress.save()

        read_count = StudentProgress.objects.filter(student=student, course_text__course=course, is_read=True).count()

        if read_count == course.texts.count():
            certificate, created = Certificate.objects.get_or_create(course_user=student, name=f"Certificate for {course.name}")
            if created:
                certificate.save()
            return Response({"message": "Student finished the course!","certificate_name": certificate.name}, status=status.HTTP_200_OK)
        return Response({"message": "Text marked as read", "read_count": read_count}, status=status.HTTP_200_OK)

class MyCoursesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = get_object_or_404(Student, user=request.user)
        courses = student.joined_courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)