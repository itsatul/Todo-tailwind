from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from django.contrib.auth.models import User
from oauth2_provider.generators import generate_client_secret
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates an OAuth2 application for the Todo app'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Get or create the user
                user, created = User.objects.get_or_create(
                    username='atul',
                    defaults={
                        'is_staff': True,
                        'is_superuser': True
                    }
                )
                
                # Generate a client secret
                client_secret = generate_client_secret()
                
                # Create the OAuth2 application
                app, created = Application.objects.get_or_create(
                    name='Todo App',
                    defaults={
                        'user': user,
                        'client_type': 'confidential',
                        'authorization_grant_type': 'password',
                        'redirect_uris': 'http://localhost:3000',
                        'client_secret': client_secret
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS('Successfully created OAuth2 application'))
                    self.stdout.write(f'Client ID: {app.client_id}')
                    self.stdout.write(f'Client Secret: {client_secret}')
                else:
                    self.stdout.write(self.style.SUCCESS('OAuth2 application already exists'))
                    self.stdout.write(f'Client ID: {app.client_id}')
                    self.stdout.write(f'Client Secret: {app.client_secret}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating OAuth2 application: {str(e)}')) 