import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here


from main_app.models import Student


# Run and print your queries


def add_students():
    details = [
        ['FC5204', 'John', 'Doe', '15/05/1995', 'john.doe@university.com'],
        ['FE0054', 'Jane', 'Smith', 'null', 'jane.smith@university.com'],
        ['FH2014', 'Alice', 'Johnson', '10/02/1998', 'alice.johnson@university.com'],
        ['FH2015', 'Bob', 'Wilson', '25/11/1996', 'bob.wilson@university.com'],
    ]

    new_students = []

    for student in details:
        birth_date = None
        if student[3] and student[3].lower() != 'null':
            birth_date = datetime.strptime(student[3], '%d/%m/%Y').date()
        new_students.append(Student(
            student_id=student[0],
            first_name=student[1],
            last_name=student[2],
            birth_date=birth_date,
            email=student[4]
        ))

    Student.objects.bulk_create(new_students)