import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import Students

print("Student Login Credentials:")
print("=" * 40)

students = Students.objects.all()
for student in students:
    print(f"Name: {student.admin.first_name} {student.admin.last_name}")
    print(f"Username: {student.admin.username}")
    print(f"Email: {student.admin.email}")
    print("Password: [Hashed - Not retrievable in plain text]")
    print("-" * 30)

print(f"\nTotal Students: {students.count()}")

# Note: Passwords are securely hashed and cannot be displayed in plain text.
# If you need to reset passwords, use Django admin or create a management command.