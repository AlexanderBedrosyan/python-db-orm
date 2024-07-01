import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here


from main_app.models import Student

def get_students_info():
    all_students = Student.objects.all()
    return '\n'.join([f'Student №{student.pk}: {student.first_name} {student.last_name}; Email: {student.email}' for student in all_students])
