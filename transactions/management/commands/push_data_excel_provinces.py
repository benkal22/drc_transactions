from typing import Any
from django.core.management.base import BaseCommand
from ...models import Province  # Assurez-vous d'importer correctement votre modèle Province depuis votre application

import pandas as pd
import os

class Command(BaseCommand):
    help = 'Import data from Excel to Province table'

    def handle(self, *args: Any, **options: Any) -> str | None:
        # Chemin vers le fichier Excel
        repertoire_script = os.path.dirname(os.path.abspath(__file__))
        file_name = "provinces_drc.xlsx"
        path_file = os.path.join(repertoire_script, file_name)
        
        # Lecture des données depuis le fichier Excel
        data = pd.read_excel(path_file)

        # Parcours des lignes du dataframe
        for index, row in data.iterrows():
            province = Province(
                name=row['name'],
                chef_lieu=row['chef_lieu'],
                superficie=row['superficie'],
                population=row['population'],
                rank=row['rank']
            )
            province.save()

        self.stdout.write(self.style.SUCCESS('Données importées avec succès depuis Excel vers la table Province'))

