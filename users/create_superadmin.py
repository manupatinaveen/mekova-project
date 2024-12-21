from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Create a superadmin user'

    def handle(self, *args, **kwargs):
        email = input("Enter email for superadmin: ")
        full_name = input("Enter full name for superadmin: ")
        password = input("Enter password: ")
        user = User.objects.create_superuser(email=email, full_name=full_name, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superadmin created: {user.email}'))
