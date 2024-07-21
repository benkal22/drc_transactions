from typing import Any
from django.core.management.base import BaseCommand
from ...models import UniqueSector

class Command(BaseCommand):
    help = 'Nettoie les espaces de fin des labels des secteurs uniques.'

    def handle(self, *args, **kwargs):
        # Récupérer tous les objets UniqueSector
        secteurs = UniqueSector.objects.all()

        modifie_count = 0
        for secteur in secteurs:
            # Enlever les espaces de fin du champ 'sector_label'
            if secteur.sector_label != secteur.sector_label.rstrip():
                secteur.sector_label = secteur.sector_label.rstrip()
                secteur.save()
                modifie_count += 1

        self.stdout.write(self.style.SUCCESS(f'Nettoyage terminé. {modifie_count} secteurs modifiés.'))




