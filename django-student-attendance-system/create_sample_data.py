import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import *

# Create course
course, created = Courses.objects.get_or_create(course_name="Computer Science")
print(f"Course: {course}")

# Create session
session, created = SessionYearModel.objects.get_or_create(session_start_year="2026-01-01", session_end_year="2027-12-31")
print(f"Session: {session}")

# Create staff
staff_user, created = CustomUser.objects.get_or_create(
    username="staff1",
    defaults={
        "email": "staff1@gmail.com",
        "password": "pbkdf2_sha256$260000$abc123",  # hashed password for 'staff'
        "user_type": 2,
        "first_name": "John",
        "last_name": "Doe"
    }
)
if created:
    staff_user.set_password("staff")
    staff_user.save()
staff_obj, created = Staffs.objects.get_or_create(admin=staff_user, defaults={"address": "Address"})
print(f"Staff: {staff_user}")

# Create subject
subject, created = Subjects.objects.get_or_create(
    subject_name="Math",
    defaults={
        "course_id": course,
        "staff_id": staff_obj
    }
)
print(f"Subject: {subject}")

# Create student
student_user, created = CustomUser.objects.get_or_create(
    username="student1",
    defaults={
        "email": "student1@gmail.com",
        "password": "pbkdf2_sha256$260000$abc123",
        "user_type": 3,
        "first_name": "Jane",
        "last_name": "Smith"
    }
)
if created:
    student_user.set_password("student")
    student_user.save()
student_obj, created = Students.objects.get_or_create(
    admin=student_user,
    defaults={
        "gender": "Female",
        "profile_pic": "",
        "address": "Address",
        "course_id": course,
        "session_year_id": session
    }
)
print(f"Student: {student_user}")

print("Sample data created.")