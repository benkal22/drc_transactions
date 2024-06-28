from django.core.management.base import BaseCommand
from transactions.models import Product, UniqueSector  # Remplacez 'myapp' par le nom de votre application

class Command(BaseCommand):
    help = 'Store unique product values in UniqueSector table'

    def handle(self, *args, **kwargs):
        unique_products = Product.objects.values('sector_code', 'sector_label').distinct()
        
        UniqueSector.objects.all().delete()  # Pour réinitialiser la table fictive
        for product in unique_products:
            UniqueSector.objects.create(
                sector_code=product['sector_code'],
                sector_label=product['sector_label']
            )
        self.stdout.write(self.style.SUCCESS('Successfully stored unique product values in UniqueSector table'))
