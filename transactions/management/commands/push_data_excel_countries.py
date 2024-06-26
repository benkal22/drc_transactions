# transactions/management/commands/push_data_excel_countries.py

from typing import Any
from django.core.management.base import BaseCommand
from ...models import Country

import pandas as pd
import os

class Command(BaseCommand):
    help = 'Imports data from Excel to the Country model'

    def handle(self, *args: Any, **options: Any) -> str:
        # Chemin vers le fichier Excel
        file_name = "worldcountries.xlsx"
        path_file = os.path.join(os.path.dirname(__file__), file_name)

        # Lecture des données depuis le fichier Excel
        data = pd.read_excel(path_file)

        # Importation des données dans la base de données
        for index, row in data.iterrows():
            country = Country(
                country=row['country'],
                iso2=row['iso2'],
                iso3=row['iso3'],
                # id=row['id']
            )
            country.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully from Excel to the database'))
