# Admin user management command
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        username = 'admin'
        password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin123')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, 'admin@example.com', password)
            self.stdout.write('Superuser created')
        else:
            self.stdout.write('Superuser already exists')