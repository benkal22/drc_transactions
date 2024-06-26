from typing import Any
from django.core.management.base import BaseCommand
from ...models import Product

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        # Récupérer tous les enregistrements de la table Product
        products = Product.objects.all()

        # Parcourir chaque enregistrement et supprimer les espaces de fin dans les champs de texte
        for product in products:
            product.sector_label = product.sector_label.rstrip()
            product.activity_label = product.activity_label.rstrip()
            product.product_label = product.product_label.rstrip()
            product.save()

        # self.stdout.write(path_file)
        self.stdout.write(self.style.SUCCESS('Espace de fin enlevés dans les données'))






