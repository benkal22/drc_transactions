import random
import re
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from transactions.models import Producer, Product, UniqueSector, Country, Province
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

class Command(BaseCommand):
    help = 'Assign random sector labels, products, country, province, and other fields to producers'

    def handle(self, *args, **kwargs):
        producers = Producer.objects.all()
        unique_sectors = UniqueSector.objects.all()
        congo_kinshasa = Country.objects.get(id=20)  # Assurez-vous que l'id correspond à "Congo (Kinshasa)"
        provinces = Province.objects.all()

        for producer in producers:
            # Assign Congo (Kinshasa) as the country
            producer.country = congo_kinshasa

            # Randomly choose a province for the producer
            province = random.choice(provinces)
            producer.province = province

            # Randomly choose a sector for the producer
            sector = random.choice(unique_sectors)
            producer.sector_label = sector

            # Assign random values to other fields
            producer.company_name = generate_company_name(sector.sector_label)
            producer.manager_name = generate_manager_name()
            producer.tax_code = generate_tax_code()
            producer.nrc = generate_nrc()
            producer.nat_id = generate_nat_id()
            producer.address = generate_address()
            producer.email = generate_email(producer.company_name)
            producer.phone_number = generate_phone_number()

            # Generate a valid initial_balance
            producer.initial_balance = generate_initial_balance()

            # Set current_balance to the same as initial_balance
            producer.current_balance = producer.initial_balance

            # Generate a default or random photo
            producer.photo = generate_random_image()

            try:
                producer.save()
            except InvalidOperation as e:
                self.stdout.write(self.style.ERROR(f'Failed to save producer {producer.id}: {e}'))
                continue

            # Filter products based on the chosen sector label
            products = Product.objects.filter(sector_label=sector.sector_label)

            # Assign random products to the producer
            if products.exists():  # Ensure there are products to choose from
                products_to_assign = random.sample(list(products), random.randint(1, len(products)))
                producer.product.set(products_to_assign)
            else:
                producer.product.clear()  # Clear products if none match the sector

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

def generate_email(company_name):
    # Nettoyer le nom de la société pour créer une partie locale valide
    local_part = re.sub(r'[^a-zA-Z0-9]', '', company_name.lower())
    domain = 'example.com'
    return f'{local_part}@{domain}'

def generate_phone_number():
    return f'+243{random.randint(700000000, 799999999)}'

def generate_initial_balance():
    try:
        balance = Decimal(random.uniform(500000.00, 1000000000.00))
        # Assurez-vous que la valeur respecte les contraintes du champ DecimalField
        return balance.quantize(Decimal('0.01'))
    except InvalidOperation:
        return Decimal('0.00')  # Valeur par défaut en cas d'erreur

def generate_random_image():
    # Generate a random image
    width, height = 100, 100
    image = Image.new('RGB', (width, height), color='gray')
    output = BytesIO()
    image.save(output, format='JPEG', quality=85)
    output.seek(0)
    return ContentFile(output.getvalue(), 'default_image.jpg')
