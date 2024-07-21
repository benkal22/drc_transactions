# transactions/management/commands/create_suppliers_clients.py

import random
from django.core.management.base import BaseCommand
from transactions.models import Supplier, Client, Product, UniqueSector, Country, Province

class Command(BaseCommand):
    help = 'Update supplier names from company_name and clear company_name'

    def handle(self, *args, **kwargs):
        # Récupérer tous les suppliers avec un nom de société
        suppliers = Supplier.objects.filter(category='enterprise', company_name__isnull=False)
        
        for supplier in suppliers:
            # Affecter la valeur de company_name à name
            supplier.name = supplier.company_name
            # Effacer la valeur de company_name
            supplier.company_name = None
            # Sauvegarder les modifications
            supplier.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated supplier names and cleared company_name'))

# import random
# from django.core.management.base import BaseCommand
# from transactions.models import Supplier, Client, Product, UniqueSector, Country, Province

# class Command(BaseCommand):
#     help = 'Update client names from company_name and clear company_name'

#     def handle(self, *args, **kwargs):
#         # Récupérer tous les clients avec un nom de société
#         clients = Client.objects.filter(category='enterprise', company_name__isnull=False)
        
#         for client in clients:
#             # Affecter la valeur de company_name à name
#             client.name = client.company_name
#             # Effacer la valeur de company_name
#             client.company_name = None
#             # Sauvegarder les modifications
#             client.save()

#         self.stdout.write(self.style.SUCCESS('Successfully updated client names and cleared company_name'))
