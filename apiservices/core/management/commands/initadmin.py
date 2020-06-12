
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        c = User(username=settings.ADMIN_USERNAME)
        c.set_password(settings.ADMIN_PWD)
        c.is_superuser = True
        c.is_staff = True
        c.save()


# from django.contrib.auth import get_user_model

# User = get_user_model()

# class Command(BaseCommand):

#     def handle(self, *args, **options):
#         User.objects.create_superuser(email="raja@hpe.com",password="00000000")