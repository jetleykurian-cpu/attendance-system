import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import *

# Clear all data
AttendanceReport.objects.all().delete()
Attendance.objects.all().delete()
Students.objects.all().delete()
Subjects.objects.all().delete()
Courses.objects.all().delete()
SessionYearModel.objects.all().delete()
Staffs.objects.all().delete()
AdminHOD.objects.all().delete()
CustomUser.objects.filter(user_type__in=[1,2,3,4]).delete()  # Keep superuser if any

print("All data cleared.")