from django.contrib import admin
from django.urls import path, include
from .views import UserRegisterationAPIView, UserRegisterationAPIView, UserLoginAPIView, InstructorAPIView, InstructorDetailAPIView, StudentAPIView, StudentDetailAPIView

urlpatterns = [
    path('register/', UserRegisterationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('students/', StudentAPIView.as_view(), name='instructor-list'),
    path('students/<int:pk>/', StudentDetailAPIView.as_view(), name='instructor-detail'),
    path('instructors/', InstructorAPIView.as_view(), name='student-list'),
    path('instructors/<int:pk>/', InstructorDetailAPIView.as_view(), name='student-detail'),
]