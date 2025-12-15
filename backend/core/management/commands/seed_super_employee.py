from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password
from core.models import User
import os

class Command(BaseCommand):
    help = 'Seed a single super employee (if none exists)'

    def handle(self, *args, **options):
        existing = User.objects.filter(role='super_employee').first()
        if existing:
            self.stdout.write(self.style.WARNING('Super employee already exists: %s' % existing.username))
            return

        username = os.getenv('SUPER_EMPLOYEE_USERNAME', 'chief')
        email = os.getenv('SUPER_EMPLOYEE_EMAIL', 'chief@university.local')
        full_name = os.getenv('SUPER_EMPLOYEE_FULLNAME', 'المسؤول الرئيسي')
        password = os.getenv('SUPER_EMPLOYEE_PASSWORD', 'StrongAdmin@2025')

        with transaction.atomic():
            user = User.objects.create(
                full_name=full_name,
                username=username,
                email=email,
                password_hash=make_password(password),
                role='super_employee',
            )
        self.stdout.write(self.style.SUCCESS('Super employee created: %s' % user.username))
