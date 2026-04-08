from student_management_app.models import CustomUser
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a superuser'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the superuser')
        parser.add_argument('--email', type=str, help='Email for the superuser')
        parser.add_argument('--password', type=str, help='Password for the superuser')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(username='admin', email='admin@example.com', password='admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))