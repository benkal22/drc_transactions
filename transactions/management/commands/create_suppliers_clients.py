# transactions/management/commands/create_suppliers_clients.py

# import random
# from django.core.management.base import BaseCommand
# from transactions.models import Producer, Supplier, Client, ProducerSupplier, ProducerClient, Country, Province

# class Command(BaseCommand):
#     help = 'Create random suppliers and clients, and assign them to producers'

#     def handle(self, *args, **kwargs):
#         producers = Producer.objects.all()
#         countries = Country.objects.all()
#         provinces = Province.objects.all()

#         # Nombre total d'entités à créer
#         total_suppliers = 100  # Total de fournisseurs
#         total_clients = 200  # Total de clients

#         # Calcul du nombre d'entités locales
#         local_suppliers_count = int(total_suppliers * 0.8)
#         local_clients_count = int(total_clients * 0.8)

#         # Création des fournisseurs locaux
#         for _ in range(local_suppliers_count):
#             country = Country.objects.get(country='Congo (Kinshasa)')
#             province = random.choice(provinces) if country.country == 'Congo (Kinshasa)' else None
#             Supplier.objects.create(
#                 category=random.choice(['enterprise', 'individual']),
#                 company_name=f"Supplier {random.randint(100, 999)}",
#                 email=f"supplier_{random.randint(100, 999)}@example.com",
#                 country=country,
#                 province=province
#             )

#         # Création des clients locaux
#         for _ in range(local_clients_count):
#             country = Country.objects.get(country='Congo (Kinshasa)')
#             province = random.choice(provinces) if country.country == 'Congo (Kinshasa)' else None
#             Client.objects.create(
#                 category=random.choice(['enterprise', 'individual']),
#                 company_name=f"Client {random.randint(100, 999)}",
#                 email=f"client_{random.randint(100, 999)}@example.com",
#                 country=country,
#                 province=province
#             )

#         # Calcul du nombre d'entités étrangères restantes à créer
#         foreign_suppliers_count = total_suppliers - local_suppliers_count
#         foreign_clients_count = total_clients - local_clients_count

#         # Création des fournisseurs étrangers
#         for _ in range(foreign_suppliers_count):
#             country = random.choice(countries.exclude(country='Congo (Kinshasa)'))
#             province = random.choice(provinces) if country.country == 'Congo (Kinshasa)' else None
#             Supplier.objects.create(
#                 category=random.choice(['enterprise', 'individual']),
#                 company_name=f"Supplier {random.randint(100, 999)}",
#                 email=f"supplier_{random.randint(100, 999)}@example.com",
#                 country=country,
#                 province=province
#             )

#         # Création des clients étrangers
#         for _ in range(foreign_clients_count):
#             country = random.choice(countries.exclude(country='Congo (Kinshasa)'))
#             province = random.choice(provinces) if country.country == 'Congo (Kinshasa)' else None
#             Client.objects.create(
#                 category=random.choice(['enterprise', 'individual']),
#                 company_name=f"Client {random.randint(100, 999)}",
#                 email=f"client_{random.randint(100, 999)}@example.com",
#                 country=country,
#                 province=province
#             )

#         # Assignation aléatoire des fournisseurs et des clients à chaque producteur
#         for producer in producers:
#             suppliers_to_assign = random.sample(list(Supplier.objects.all()), random.randint(1, 3))  # Assigner 1 à 3 fournisseurs
#             clients_to_assign = random.sample(list(Client.objects.all()), random.randint(1, 5))  # Assigner 1 à 5 clients

#             for supplier in suppliers_to_assign:
#                 ProducerSupplier.objects.create(producer=producer, supplier=supplier)

#             for client in clients_to_assign:
#                 ProducerClient.objects.create(producer=producer, client=client)

#             self.stdout.write(self.style.SUCCESS(f'Created and assigned suppliers and clients to producer {producer.id}'))

import random
from django.core.management.base import BaseCommand
from transactions.models import Supplier, Client, Product, UniqueSector, Country, Province

class Command(BaseCommand):
    help = 'Assign random sector labels, products, country, province, and other fields to suppliers and clients'

    def handle(self, *args, **kwargs):
        suppliers = Supplier.objects.all()
        clients = Client.objects.all()
        unique_sectors = UniqueSector.objects.all()
        countries = Country.objects.all()
        provinces = Province.objects.all()
        products = Product.objects.all()

        for supplier in suppliers:
            # Assign Congo (Kinshasa) as the country for all suppliers
            congo_kinshasa = countries.get(country='Congo (Kinshasa)')
            supplier.country = congo_kinshasa

            # Randomly choose a province for the supplier
            supplier.province = random.choice(provinces)

            # Randomly choose a sector for the supplier
            sector = random.choice(unique_sectors)
            supplier.sector_label.add(sector)  # Assigning the instance of UniqueSector

            # Assign random values to other fields
            if supplier.category == 'enterprise':
                supplier.company_name = generate_company_name(sector.sector_label)
            supplier.manager_name = generate_manager_name()
            supplier.tax_code = generate_tax_code()
            supplier.nrc = generate_nrc()
            supplier.nat_id = generate_nat_id()
            supplier.address = generate_address()
            supplier.phone_number = generate_phone_number()
            supplier.email = generate_email(supplier.company_name if supplier.category == 'enterprise' else None)

            # Filter products based on the chosen sector label
            filtered_products = products.filter(sector_label=sector)

            # Assign random products to the supplier if products exist
            if filtered_products.exists():
                products_to_assign = random.sample(list(filtered_products), random.randint(1, len(filtered_products)))
                supplier.product.set(products_to_assign)

            supplier.save()

            self.stdout.write(self.style.SUCCESS(f'Assigned data to supplier {supplier.id}'))

        for client in clients:
            # Assign Congo (Kinshasa) as the country for all clients
            congo_kinshasa = countries.get(country='Congo (Kinshasa)')
            client.country = congo_kinshasa

            # Randomly choose a province for the client
            client.province = random.choice(provinces)

            # Randomly choose a sector for the client
            sector = random.choice(unique_sectors)
            client.sector_label.add(sector)  # Assigning the instance of UniqueSector

            # Assign random values to other fields
            if client.category == 'enterprise':
                client.company_name = generate_company_name(sector.sector_label)
            client.manager_name = generate_manager_name()
            client.tax_code = generate_tax_code()
            client.nrc = generate_nrc()
            client.nat_id = generate_nat_id()
            client.address = generate_address()
            client.phone_number = generate_phone_number()
            client.email = generate_email(client.company_name if client.category == 'enterprise' else None)

            # Filter products based on the chosen sector label
            filtered_products = products.filter(sector_label=sector)

            # Assign random products to the client if products exist
            if filtered_products.exists():
                products_to_assign = random.sample(list(filtered_products), random.randint(1, len(filtered_products)))
                client.product.set(products_to_assign)

            client.save()

            self.stdout.write(self.style.SUCCESS(f'Assigned data to client {client.id}'))

def generate_company_name(sector_label):
    prefixes = ['Société', 'Entreprise', 'Compagnie', 'Groupe', 'Association']
    suffixes = ['Industrielle', 'Commerciale', 'Technologique', 'Agricole', 'de Services']
    return f'{random.choice(prefixes)} {sector_label} {random.choice(suffixes)}'

def generate_manager_name():
    first_names = ['Jean', 'Pierre', 'Claude', 'Marie', 'Christine']
    last_names = ['Kabila', 'Mukendi', 'Makasi', 'Lumumba', 'Kasongo']
    return f'{random.choice(first_names)} {random.choice(last_names)}'

def generate_tax_code():
    return f'TAX{random.randint(1000, 9999)}'

def generate_nrc():
    return f'NRC{random.randint(1000, 9999)}'

def generate_nat_id():
    return f'NAT{random.randint(1000, 9999)}'

def generate_address():
    streets = ['Avenue Kasai', 'Rue Lubumbashi', 'Boulevard Kigali', 'Chemin Kananga']
    return f'{random.choice(streets)}, Quartier {random.randint(1, 10)}'

def generate_phone_number():
    return f'+243{random.randint(700000000, 799999999)}'

def generate_email(company_name=None):
    if company_name:
        company_name = company_name.lower().replace(' ', '_')
        return f'{company_name}@example.com'
    return f'user{random.randint(100, 999)}@example.com'
