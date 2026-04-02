import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import Students, SessionYearModel, Courses, Subjects

print('Students:', Students.objects.count())
print('SessionYears:', SessionYearModel.objects.count())
print('Courses:', Courses.objects.count())
print('Subjects:', Subjects.objects.count())

for s in Students.objects.all()[:5]:
    print(f'Student: {s.admin.first_name} {s.admin.last_name}, Course: {s.course_id}, Session: {s.session_year_id}')

for sub in Subjects.objects.all()[:5]:
    print(f'Subject: {sub.subject_name}, Course: {sub.course_id}, Staff: {sub.staff_id}')

for sy in SessionYearModel.objects.all():
    print(f'Session: {sy.session_start_year} to {sy.session_end_year}')