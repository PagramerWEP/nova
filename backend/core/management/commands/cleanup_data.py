from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import User, ActivityRegistration, Application, EmployeeRequest, Notification, Message
from django.core.files.storage import default_storage
from django.utils import timezone
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Remove all student and employee accounts and their related data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting anything',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Get all student and employee users
        users = User.objects.filter(role__in=['student', 'employee'])
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes will be made'))
            self.stdout.write('\nThe following would be deleted:')
            self.stdout.write(f'- {users.count()} user(s) (students and employees)')
            
            # Get counts for related objects
            activity_registrations = ActivityRegistration.objects.filter(user__in=users).count()
            applications = Application.objects.filter(user__in=users).count()
            sent_requests = EmployeeRequest.objects.filter(employee__in=users).count()
            received_requests = EmployeeRequest.objects.filter(student__in=users).count()
            notifications = Notification.objects.filter(user__in=users).count()
            messages = Message.objects.filter(application__user__in=users).count()
            
            self.stdout.write(f'- {activity_registrations} activity registration(s)')
            self.stdout.write(f'- {applications} application(s)')
            self.stdout.write(f'- {sent_requests} sent employee request(s)')
            self.stdout.write(f'- {received_requests} received employee request(s)')
            self.stdout.write(f'- {notifications} notification(s)')
            self.stdout.write(f'- {messages} message(s) and attached files')
            return

        # Start transaction
        with transaction.atomic():
            # Remove files from disk (project files and message attachments)
            for app in Application.objects.filter(user__in=users).iterator():
                if app.project_file:
                    try:
                        if default_storage.exists(app.project_file.name):
                            default_storage.delete(app.project_file.name)
                    except Exception:
                        pass
            for msg in Message.objects.filter(application__user__in=users).iterator():
                if msg.attachment:
                    try:
                        if default_storage.exists(msg.attachment.name):
                            default_storage.delete(msg.attachment.name)
                    except Exception:
                        pass
            # Delete related objects first
            deleted_registrations = ActivityRegistration.objects.filter(user__in=users).delete()
            deleted_applications = Application.objects.filter(user__in=users).delete()
            deleted_sent_requests = EmployeeRequest.objects.filter(employee__in=users).delete()
            deleted_received_requests = EmployeeRequest.objects.filter(student__in=users).delete()
            deleted_notifications = Notification.objects.filter(user__in=users).delete()
            deleted_messages = Message.objects.filter(application__user__in=users).delete()
            
            # Finally, delete the users
            deleted_users = users.delete()

            # Remove orphan files (not linked records) under media directories
            def _purge_dir(subdir: str):
                base = os.path.join(settings.MEDIA_ROOT, subdir)
                if os.path.isdir(base):
                    for root, _dirs, files in os.walk(base):
                        for fn in files:
                            fp = os.path.join(root, fn)
                            try:
                                os.remove(fp)
                            except Exception:
                                pass

            _purge_dir('project_files')
            _purge_dir('message_files')
            
            self.stdout.write(self.style.SUCCESS('Successfully deleted:'))
            self.stdout.write(f'- {deleted_users[0]} user(s) (students and employees)')
            self.stdout.write(f'- {deleted_registrations[0]} activity registration(s)')
            self.stdout.write(f'- {deleted_applications[0]} application(s)')
            self.stdout.write(f'- {deleted_sent_requests[0]} sent employee request(s)')
            self.stdout.write(f'- {deleted_received_requests[0]} received employee request(s)')
            self.stdout.write(f'- {deleted_notifications[0]} notification(s)')
            self.stdout.write(f'- {deleted_messages[0]} message(s)')
            self.stdout.write(f'- Purged orphan files in media/project_files and media/message_files')
