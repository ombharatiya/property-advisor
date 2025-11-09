
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a superuser account'

    def handle(self, *args, **options):
        username = 'admin'
        email = settings.ADMIN_USERNAME
        password = settings.ADMIN_PASSWORD
        
        if User.objects.filter(username=username).exists():
            print(f'Admin user "{username}" already exists')
            return
            
        print(f'Creating admin account for {username} ({email})')
        admin = User.objects.create_superuser(
            email=email, 
            username=username, 
            password=password
        )
        admin.is_active = True
        admin.save()
        print('Admin account created successfully')


# from django.contrib.auth import get_user_model

# User = get_user_model()

# class Command(BaseCommand):

#     def handle(self, *args, **options):
#         User.objects.create_superuser(email="raja@hpe.com",password="00000000")