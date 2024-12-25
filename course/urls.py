from django.contrib import admin
from django.urls import path, include
from .views import CourseAPIView, CourseDetailAPIView, MyCoursesAPIView, JoinCourseAPIView , CourseTextAPIView, MarkTextAsReadAPIView

urlpatterns = [
    path('', CourseAPIView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('<int:course_id>/join/', JoinCourseAPIView.as_view(), name='join-course'),
    path('<int:course_id>/texts/', CourseTextAPIView.as_view(), name='course-texts'),
    path('<int:text_id>/read/', MarkTextAsReadAPIView.as_view(), name='mark-read'),
    path('my/', MyCoursesAPIView.as_view(), name='my-courses'),
]