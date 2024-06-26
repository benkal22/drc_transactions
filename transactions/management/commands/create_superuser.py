from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Create a superuser if none exist'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            try:
                User.objects.create_superuser(
                    username='benkal',
                    email='admin@example.com',
                    password='diansosa2020'
                )
                self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING('Superuser already exists'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
