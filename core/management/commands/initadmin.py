from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create default admin if not exists"

    def handle(self, *args, **kwargs):
        username = os.getenv("DJANGO_ADMIN_USER", "Varun)5126")
        email = os.getenv("DJANGO_ADMIN_EMAIL", "malthumkarvarun@gmail.com")
        password = os.getenv("DJANGO_ADMIN_PASSWORD", "Varun05126")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS("✅ Admin user created"))
        else:
            self.stdout.write("ℹ️ Admin already exists")