from django.contrib import admin
from .models import Course, Certificate, StudentProgress, CourseText

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'instructor', 'created_at']

admin.site.register(Course, CourseAdmin)

class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_user', 'created_at']

admin.site.register(Certificate, CertificateAdmin)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'course_text', 'is_read', 'created_at']

admin.site.register(StudentProgress, StudentProgressAdmin)

class CourseTextAdmin(admin.ModelAdmin):
    list_display = ['course', 'created_at']
admin.site.register(CourseText, CourseTextAdmin)
