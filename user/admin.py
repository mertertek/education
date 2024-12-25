from django.contrib import admin
from .models import CustomUser, Instructor, Student

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_instructor', 'is_student', 'is_active', 'is_staff', 'date_joined']

admin.site.register(CustomUser, CustomUserAdmin)

class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

admin.site.register(Instructor, InstructorAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

admin.site.register(Student, StudentAdmin)
