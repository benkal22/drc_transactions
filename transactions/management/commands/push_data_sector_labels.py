from django.core.management.base import BaseCommand
from transactions.models import UniqueSector, Product

class Command(BaseCommand):
    help = 'Push data for sector labels'

    def handle(self, *args, **kwargs):
        # Query all products
        products = Product.objects.all()

        # Create a set to store unique (sector_code, sector_label) tuples
        unique_sectors = set()

        for product in products:
            sector_code = product.sector_code
            sector_label = product.sector_label

            # Check if this (sector_code, sector_label) tuple is already in the set
            if (sector_code, sector_label) not in unique_sectors:
                unique_sectors.add((sector_code, sector_label))

                # Create UniqueSector entry
                UniqueSector.objects.create(sector_code=sector_code, sector_label=sector_label)
                self.stdout.write(self.style.SUCCESS(f'Sector "{sector_label}" created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Sector "{sector_label}" already exists'))

