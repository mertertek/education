from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Course, CourseText
from .views import CourseTextAPIView


@receiver(post_save, sender=CourseText)
def update_total_text_count_on_create(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        course.total_text_count = course.texts.count()
        course.save()

