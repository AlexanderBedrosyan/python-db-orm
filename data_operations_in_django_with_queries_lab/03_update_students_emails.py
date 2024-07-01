import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here


from main_app.models import Student


# Run and print your queries

def update_students_emails():
    all_student = Student.objects.all()
    updated_students = []

    for student in all_student:
        student.email = student.email.split('@')[0] + '@uni-students.com'
        updated_students.append(student)

    Student.objects.bulk_update(updated_students, ['email'])