import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import CustomUser, AdminHOD

# Check if user exists
if CustomUser.objects.filter(email='admin@gmail.com').exists():
    print("Admin user already exists.")
else:
    # Create HOD user
    user = CustomUser.objects.create_user(username='admin', email='admin@gmail.com', password='admin', user_type=1, first_name='Admin', last_name='')
    user.save()

    # Create AdminHOD
    hod = AdminHOD(admin=user)
    hod.save()

    print("HOD user created: admin@gmail.com / admin")