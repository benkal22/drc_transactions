from django.core.management.base import BaseCommand
from transactions.models import Product, UniqueProduct  # Remplacez 'myapp' par le nom de votre application

class Command(BaseCommand):
    help = 'Store unique product values in UniqueProduct table'

    def handle(self, *args, **kwargs):
        unique_products = Product.objects.values('sector_code', 'sector_label', 'activity_code', 'activity_label').distinct()
        
        UniqueProduct.objects.all().delete()  # Pour réinitialiser la table fictive
        for product in unique_products:
            UniqueProduct.objects.create(
                sector_code=product['sector_code'],
                sector_label=product['sector_label'],
                activity_code=product['activity_code'],
                activity_label=product['activity_label']
            )
        self.stdout.write(self.style.SUCCESS('Successfully stored unique product values in UniqueProduct table'))
