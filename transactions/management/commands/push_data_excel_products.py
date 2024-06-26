from typing import Any
from django.core.management.base import BaseCommand
from ...models import Product

import pandas as pd
from sqlalchemy import create_engine
import os

#Importation des données excel de la nomenclature des secteurs d'activités 

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args: Any, **options: Any) -> str | None:
        #Lecture données excel de nomenclature des secteurs d'activités
        repertoire_script = os.path.dirname(os.path.abspath(__file__))
        file_name = "nomenclature.csv"
        path_file = os.path.join(repertoire_script, file_name)
        data = pd.read_csv(path_file, encoding="ISO-8859-1", delimiter=";")

        for index, row in data.iterrows():
            product = Product(
                sector_code = row['sector_code'],
                sector_label = row['sector_label'],
                activity_code = row['activity_code'],
                activity_label = row['activity_label'],
                product_code = row['product_code'],
                product_label = row['product_label'])
            product.save()

        self.stdout.write(self.style.SUCCESS('Données importées avec succès depuis Excel vers la base de données'))

# class Command(BaseCommand):
#     def handle(self, *args: Any, **options: Any) -> str | None:
#         # Récupérer tous les enregistrements de la table Product
#         products = Product.objects.all()

#         # Parcourir chaque enregistrement et supprimer les espaces de fin dans les champs de texte
#         for product in products:
#             product.sector_label = product.sector_label.rstrip()
#             product.activity_label = product.activity_label.rstrip()
#             product.product_label = product.product_label.rstrip()
#             product.save()

#         # self.stdout.write(path_file)
#         self.stdout.write(self.style.SUCCESS('Espace de fin enlevés dans les données'))






