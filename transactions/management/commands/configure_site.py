from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Configure le site pour l\'environnement local'

    def handle(self, *args, **options):
        site, created = Site.objects.get_or_create(id=1)
        site.domain = 'localhost:8000'  # Remplacez par votre domaine local
        site.name = 'Xchange DRC App'
        site.save()

        self.stdout.write(self.style.SUCCESS('Site configuré avec succès pour l\'environnement local'))
