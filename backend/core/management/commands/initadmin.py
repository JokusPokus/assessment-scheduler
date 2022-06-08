from django.conf import settings
from django.core.management.base import BaseCommand
from user.models import User, Organization


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin'
        password = 'admin'
        print('Creating account for %s (%s)' % (username, email))
        admin = User.objects.create_superuser(email=email, username=username, password=password)

        admin.is_active = True
        admin.is_admin = True

        code_uni = Organization.objects.get(name='CODE University')
        admin.organization = code_uni

        admin.save()
