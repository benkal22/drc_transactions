import random
from django.core.management.base import BaseCommand
from transactions.models import Producer, Product, UniqueSector, Country, Province

class Command(BaseCommand):
    help = 'Assign random sector labels, products, country, province, and other fields to producers'

    def handle(self, *args, **kwargs):
        producers = Producer.objects.all()
        unique_sectors = UniqueSector.objects.all()
        congo_kinshasa = Country.objects.get(id=20)
        provinces = Province.objects.all()

        for producer in producers:
            # Assign Congo (Kinshasa) as the country
            producer.country = congo_kinshasa

            # Randomly choose a province for the producer
            province = random.choice(provinces)
            producer.province = province

            # Randomly choose a sector for the producer
            sector = random.choice(unique_sectors)
            producer.sector_label = sector  # Assigning the instance of UniqueSector

            # Assign random values to other fields
            producer.company_name = generate_company_name(sector.sector_label)
            producer.manager_name = generate_manager_name()
            producer.tax_code = generate_tax_code()
            producer.nrc = generate_nrc()
            producer.nat_id = generate_nat_id()
            producer.address = generate_address()
            producer.phone_number = generate_phone_number()

            producer.save()

            # Filter products based on the chosen sector label
            products = Product.objects.filter(sector_label=sector.sector_label)

            # Assign random products to the producer
            products_to_assign = random.sample(list(products), random.randint(1, len(products)))
            producer.product.set(products_to_assign)

            self.stdout.write(self.style.SUCCESS(f'Assigned data to producer {producer.id}'))

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
