# Generated by Django 5.1.3 on 2024-12-24 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='total_quiz_count',
            new_name='total_text_count',
        ),
    ]
