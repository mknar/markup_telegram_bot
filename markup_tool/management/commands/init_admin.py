from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            if User.objects.count() == 0:
                User.objects.create_superuser(username=settings.ADMIN_USERNAME, password=settings.ADMIN_PASSWORD)
            else:
                print('Admin accounts can only be initialized if no Accounts exist')
        except Exception as e:
            raise CommandError(f'The following error occurred while executing the command init_admin: {e}')
