import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import Students, Courses, SessionYearModel

print("All Enrolled Students Details:")
print("=" * 50)

students = Students.objects.all()
for student in students:
    print(f"ID: {student.id}")
    print(f"Name: {student.admin.first_name} {student.admin.last_name}")
    print(f"Username: {student.admin.username}")
    print(f"Email: {student.admin.email}")
    print(f"Gender: {student.gender}")
    print(f"Address: {student.address}")
    print(f"Course: {student.course_id.course_name}")
    print(f"Session: {student.session_year_id.session_start_year} to {student.session_year_id.session_end_year}")
    print(f"Profile Pic: {student.profile_pic}")
    print(f"Created At: {student.created_at}")
    print(f"Updated At: {student.updated_at}")
    print("-" * 30)

print(f"\nTotal Students: {students.count()}")