from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.timezone import now
from django.conf import settings
from user.models import CustomUser, Instructor, Student

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    total_text_count = models.IntegerField(default=0)
    students = models.ManyToManyField(Student, related_name='joined_courses', blank=True)
    
    def __str__(self):
        return self.name

class Certificate(models.Model):
    course_user = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='certificate')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.course_user.user.name} "

class CourseText(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="texts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Text: {self.course.name} - {self.id}"

class StudentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="progress")
    course_text = models.ForeignKey(CourseText, on_delete=models.CASCADE, related_name="progress")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.name} - {self.course_text.id}"