# # Importation des modules nécessaires
# import random
# from datetime import datetime, timedelta
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from transactions.models import Producer, Supplier, Client, Product, Transaction

# class Command(BaseCommand):
#     help = 'Create random transactions for producers'

#     def handle(self, *args, **kwargs):
#         # Récupérer tous les producteurs
#         producers = Producer.objects.all()

#         for producer in producers:
#             # Récupérer les fournisseurs et clients associés à ce producteur
#             suppliers = producer.suppliers.all()
#             clients = producer.clients.all()
#             products = producer.product.all()

#             # Générer un nombre aléatoire de transactions pour chaque producteur
#             num_transactions = random.randint(5, 20)  # Nombre aléatoire de transactions

#             for _ in range(num_transactions):
#                 # Choisir aléatoirement un produit du producteur
#                 product = random.choice(products)

#                 # Choisir aléatoirement entre achat (purchase) ou vente (sale)
#                 transaction_type = random.choice(['purchase', 'sale'])

#                 # Sélectionner un fournisseur ou client selon le type de transaction
#                 if transaction_type == 'purchase':
#                     supplier = random.choice(suppliers)
#                     client = None
#                 else:
#                     supplier = None
#                     client = random.choice(clients)

#                 # Générer des valeurs aléatoires pour le prix et la quantité
#                 price = round(random.uniform(10.0, 1000.0), 2)  # Prix aléatoire entre 10 et 1000
#                 quantity = random.randint(1, 100)  # Quantité aléatoire entre 1 et 100

#                 # Déterminer la date de la transaction (dans les 30 derniers jours)
#                 days_offset = random.randint(1, 30)
#                 transaction_date = timezone.now() - timedelta(days=days_offset)

#                 # Créer la transaction
#                 Transaction.objects.create(
#                     producer=producer,
#                     product=product,
#                     type=transaction_type,
#                     supplier=supplier,
#                     client=client,
#                     price=price,
#                     quantity=quantity,
#                     currency='CDF',  # Devise par défaut
#                     date=transaction_date
#                 )

#         self.stdout.write(self.style.SUCCESS('Transactions aléatoires créées avec succès.'))


import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from transactions.models import Producer, Transaction

class Command(BaseCommand):
    help = 'Create random transactions for producers'

    def handle(self, *args, **kwargs):
        producers = Producer.objects.all()

        for producer in producers:
            suppliers = producer.suppliers.all()
            clients = producer.clients.all()
            products = producer.product.all()

            num_transactions = random.randint(5, 20)

            for _ in range(num_transactions):
                product = random.choice(products)
                transaction_type = random.choice(['purchase', 'sale'])
                supplier = random.choice(suppliers) if transaction_type == 'purchase' else None
                client = random.choice(clients) if transaction_type == 'sale' else None

                price = round(random.uniform(10.0, 1000.0), 2)
                quantity = random.randint(1, 100)
                transaction_date = timezone.now() - timedelta(days=random.randint(1, 30))

                Transaction.objects.create(
                    producer=producer,
                    product=product,
                    type=transaction_type,
                    supplier=supplier,
                    client=client,
                    price=price,
                    quantity=quantity,
                    currency='CDF',
                    date=transaction_date
                )

        self.stdout.write(self.style.SUCCESS('Transactions aléatoires créées avec succès.'))
