# transactions/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager, TransactionQuerySet,  TransactionManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ValidationError
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Modèle personnalisé pour les utilisateurs
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()
    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

# Modèle pour les pays
class Country(models.Model):
    country = models.CharField(max_length=100)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    # flag = models.CharField(max_length=10)
    flag = models.ImageField(
        upload_to="img/countries/",
        blank=True,
        null=True,
    )
    
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['country']

    def __str__(self):
        return self.country
    
    # def save(self, *args, **kwargs):
    #     if self.flag:
    #         # Ouvrir l'image avec Pillow
    #         image = Image.open(self.flag)
    #         output = BytesIO()
            
    #         # Redimensionner l'image si nécessaire
    #         image = image.resize((800, 800))  # Par exemple, redimensionner à 800x800 pixels
            
    #         # Sauvegarder l'image dans le format souhaité
    #         image.save(output, format='JPEG', quality=85)
    #         output.seek(0)
            
    #         # Créer un nouveau fichier ContentFile
    #         self.flag.save(self.flag.name, ContentFile(output.getvalue()), save=False)
        
    #     super().save(*args, **kwargs)

# Modèle pour les provinces
class Province(models.Model):
    name = models.CharField(max_length=150)
    chef_lieu = models.CharField(null=True, max_length=150)
    superficie = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    rank = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def province_default_display(self):
        return self.name or 'Kinshasa'
    
# Modèle pour les produits
class Product(models.Model):
    sector_code = models.CharField(max_length=100)
    sector_label = models.CharField(max_length=255)
    activity_code = models.CharField(max_length=100)
    activity_label = models.CharField(max_length=255)
    product_code = models.CharField(max_length=100)
    product_label = models.CharField(max_length=255)
    photo =  models.ImageField(
        upload_to="img/products/",
        blank=True,
        null=True,
    )
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['product_label']

    def __str__(self):
        return self.product_label

    def __unicode__(self):
        return self.product_label
    
    def save(self, *args, **kwargs):
        if self.photo:
            # Ouvrir l'image avec Pillow
            image = Image.open(self.photo)
            output = BytesIO()
            
            # Redimensionner l'image si nécessaire
            image = image.resize((800, 800))  # Par exemple, redimensionner à 800x800 pixels
            
            # Sauvegarder l'image dans le format souhaité
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            
            # Créer un nouveau fichier ContentFile
            self.photo.save(self.photo.name, ContentFile(output.getvalue()), save=False)
        
        super().save(*args, **kwargs)

# Modèle pour les secteurs uniques
class UniqueSector(models.Model):
    sector_code = models.CharField(max_length=50, unique=True)
    sector_label = models.CharField(max_length=100)
    photo =  models.ImageField(
        upload_to="img/sectors/",
        blank=True,
        null=True,
    )
    
    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
        unique_together = ('sector_code', 'sector_label')
        ordering = ['sector_label']

    def __str__(self):
        return f"{self.sector_label} - {self.sector_code }"
    
    def save(self, *args, **kwargs):
        if self.photo:
            # Ouvrir l'image avec Pillow
            image = Image.open(self.photo)
            output = BytesIO()
            
            # Redimensionner l'image si nécessaire
            image = image.resize((800, 800))  # Par exemple, redimensionner à 800x800 pixels
            
            # Sauvegarder l'image dans le format souhaité
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            
            # Créer un nouveau fichier ContentFile
            self.photo.save(self.photo.name, ContentFile(output.getvalue()), save=False)
        
        super().save(*args, **kwargs)

# Modèle pour les producteurs
class Producer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, editable=False)
    company_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    tax_code = models.CharField(max_length=100, blank=True, null=True)
    nrc = models.CharField(max_length=100, blank=True, null=True)
    nat_id = models.CharField(max_length=100, blank=True, null=True)
    product = models.ManyToManyField(Product)
    sector_label = models.ForeignKey(UniqueSector, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, limit_choices_to={'country': 'Congo (Kinshasa)'})
    province = models.ForeignKey('Province', on_delete=models.CASCADE, null=False, blank=False)
    is_approved = models.BooleanField(default=False)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Nouveau champ de solde
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Nouveau champ de solde
    # Relations ManyToMany avec les fournisseurs et clients à travers les modèles intermédiaires
    suppliers = models.ManyToManyField('Supplier', through='ProducerSupplier', related_name='suppliers')
    clients = models.ManyToManyField('Client', through='ProducerClient', related_name='clients')
    photo =  models.ImageField(
        upload_to="img/producers/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"

    def clean(self):
        if self.country.country == 'Congo (Kinshasa)' and not self.province:
            raise ValidationError("Province field is required for Congo (Kinshasa) country.")
        
    def __unicode__(self):
        return self.company_name

    def __str__(self):
        return self.company_name
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Si c'est une nouvelle instance
            self.current_balance = self.initial_balance
        
        if self.photo:
            # Ouvrir l'image avec Pillow
            image = Image.open(self.photo)
            output = BytesIO()
            
            # Redimensionner l'image si nécessaire
            image = image.resize((800, 800))  # Par exemple, redimensionner à 800x800 pixels
            
            # Sauvegarder l'image dans le format souhaité
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            
            # Créer un nouveau fichier ContentFile
            self.photo.save(self.photo.name, ContentFile(output.getvalue()), save=False)
        
        super().save(*args, **kwargs)

    def update_sector_labels(self):
        # Met à jour les étiquettes de secteur pour le producteur
        sector_labels = Product.objects.values_list('sector_label', flat=True).distinct()
        self.sector_label = ', '.join(sector_labels)
        self.save()

    @property
    def get_products_by_sector(self):
        # Retourne les produits du producteur par secteur
        return Product.objects.filter(sector_label=self.sector_label.sector_label)
    
    def total_sales_amount(self):
        sales = Transaction.objects.filter(producer=self, type='sale')
        total_sales = sales.aggregate(total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())))
        return total_sales['total'] if total_sales['total'] else 0

# Modèle pour les clients
class Client(models.Model):
    CATEGORY_CHOICES = [
        ('enterprise', 'Enterprise'),
        ('individual', 'Individual')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    tax_code = models.CharField(max_length=100, blank=True, null=True)
    nrc = models.CharField(max_length=100, blank=True, null=True)
    nat_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    product = models.ManyToManyField(Product, blank=True, null=True)
    sector_label = models.ManyToManyField(UniqueSector, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    photo =  models.ImageField(
        upload_to="img/clients/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        
    def save(self, *args, **kwargs):
        if self.category == 'individual':
            self.manager_name = None
            self.tax_code = None
            self.nrc = None
            self.nat_id = None
        
        if self.photo:
            # Ouvrir l'image avec Pillow
            image = Image.open(self.photo)
            output = BytesIO()
            
            # Redimensionner l'image si nécessaire
            image = image.resize((800, 800))  # Par exemple, redimensionner à 800x800 pixels
            
            # Sauvegarder l'image dans le format souhaité
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            
            # Créer un nouveau fichier ContentFile
            self.photo.save(self.photo.name, ContentFile(output.getvalue()), save=False)
        
        super().save(*args, **kwargs)

    def __unicode__(self):
        return self.name if self.name else "No name"

    def __str__(self):
        return self.name if self.name else "No name"
    
    def update_total_sales(self):
        self.total_sales = sum(transaction.price for transaction in self.transaction_set.filter(type='sale'))
        self.save()
    
    def clean(self):
        # Vérifier l'unicité du nom pour cette catégorie
        if self.category == 'individual':
            if self.name:
                existing_clients = Client.objects.filter(name=self.name, category='individual')
                if self.pk:
                    existing_clients = existing_clients.exclude(pk=self.pk)
                if existing_clients.exists():
                    raise ValidationError(f"Un client individuel avec le nom '{self.name}' existe déjà.")
        elif self.category == 'enterprise':
            if self.name:
                existing_clients = Client.objects.filter(name=self.name, category='enterprise')
                if self.pk:
                    existing_clients = existing_clients.exclude(pk=self.pk)
                if existing_clients.exists():
                    raise ValidationError(f"Une entreprise avec le nom '{self.name}' existe déjà.")

        # Valider également d'autres champs comme la province pour le Congo (Kinshasa)
        if self.country.country == 'Congo (Kinshasa)' and not self.province:
            raise ValidationError("Le champ province est requis pour le pays Congo (Kinshasa).")
    
    def total_sales_with_currency(self):
        return f"{self.total_sales} {self.get_country_currency_display()}"

# Modèle pour les fournisseurs
class Supplier(models.Model):
    CATEGORY_CHOICES = [
        ('enterprise', 'Enterprise'),
        ('individual', 'Individual')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    tax_code = models.CharField(max_length=100, blank=True, null=True)
    nrc = models.CharField(max_length=100, blank=True, null=True)
    nat_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    product = models.ManyToManyField(Product,  blank=True, null=True)
    sector_label = models.ManyToManyField(UniqueSector,  blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    photo =  models.ImageField(
        upload_to="img/suppliers/",
        blank=True,
        null=True,
    )
    

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __unicode__(self):
        return self.name if self.name else "No name"

    def __str__(self):
        return self.name if self.name else "No name"
    
    def get_value_or_default(self, field, default="Non spécifié"):
        value = getattr(self, field)
        return value if value is not None else default
    
    def save(self, *args, **kwargs):
        if self.category == 'individual':
            self.manager_name = None
            self.tax_code = None
            self.nrc = None
            self.nat_id = None
        
        if self.photo:
            # Ouvrir l'image avec Pillow
            image = Image.open(self.photo)
            output = BytesIO()
            
            # Redimensionner l'image si nécessaire
            image = image.resize((800, 800))  # Par exemple, redimensionner à 800x800 pixels
            
            # Sauvegarder l'image dans le format souhaité
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            
            # Créer un nouveau fichier ContentFile
            self.photo.save(self.photo.name, ContentFile(output.getvalue()), save=False)
        
        super().save(*args, **kwargs)
        
    def update_total_purchases(self):
        self.total_purchases = sum(transaction.price for transaction in self.transaction_set.filter(type='purchase'))
        self.save()
    
    def clean(self):
        # Vérifier l'unicité du nom pour cette catégorie
        if self.category == 'individual':
            if self.name:
                existing_suppliers = Supplier.objects.filter(name=self.name, category='individual')
                if self.pk:
                    existing_suppliers = existing_suppliers.exclude(pk=self.pk)
                if existing_suppliers.exists():
                    raise ValidationError(f"Un fournisseur individuel avec le nom '{self.name}' existe déjà.")
        elif self.category == 'enterprise':
            if self.name:
                existing_suppliers = Supplier.objects.filter(name=self.name, category='enterprise')
                if self.pk:
                    existing_suppliers = existing_suppliers.exclude(pk=self.pk)
                if existing_suppliers.exists():
                    raise ValidationError(f"Une entreprise fournisseur avec le nom '{self.name}' existe déjà.")

        # Valider également d'autres champs comme la province pour le Congo (Kinshasa)
        if self.country.country == 'Congo (Kinshasa)' and not self.province:
            raise ValidationError("Le champ province est requis pour le pays Congo (Kinshasa).")
    
    @property
    def total_purchases_amount(self):
        purchases = Transaction.objects.filter(supplier=self, type='purchase').aggregate(
            total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField()))
        )
        return purchases['total'] or 0
    
    def get_details(self):
        details = {
            'product': ', '.join(p.name for p in self.product.all()),
            'manager_name': self.manager_name,
            'tax_code': self.tax_code,
            'nrc': self.nrc,
            'nat_id': self.nat_id,
            'name': self.name,
            'address': self.address,
            'email': self.email,
            'phone_number': self.phone_number,
            'country': self.country.country,
            'province': self.province.name if self.province else None,
            'total_purchases': self.total_purchases,
            'category': self.category,
        }
        return details

# Modèle intermédiaire pour les relations Producer-Supplier
class ProducerSupplier(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Producteur-Fournisseur"
        verbose_name_plural = "Producteurs-Fournisseurs"

    def __str__(self):
        return f"{self.producer} - {self.supplier}"

# Modèle intermédiaire pour les relations Producer-Client
class ProducerClient(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Producteur-Client"
        verbose_name_plural = "Producteurs-Clients"

    def __str__(self):
        return f"{self.producer} - {self.client}"

# Modèle pour les transactions
class Transaction(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    TRANSACTION_TYPE_CHOICES = [
        ('purchase', 'Achat'),
        ('sale', 'Vente')
    ]
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('CDF', 'Congolese Franc'),
        ('EUR', 'Euro')
    ]
    UNIT_OF_MEASURE_CHOICES = [
        ('kg', 'Kilogramme'),
        ('g', 'Gramme'),
        ('lb', 'Livre'),
        ('l', 'Litre'),
        ('ml', 'Millilitre'),
        ('m3', 'Mètre cube'),
        ('unit', 'Unité'),
        ('box', 'Boîte'),
        ('piece', 'Pièce'),
        ('m', 'Mètre'),
        ('cm', 'Centimètre'),
        ('mm', 'Millimètre'),
        ('inch', 'Pouce'),
        ('ft', 'Pied'),
        ('yd', 'Yard'),
        ('tonne', 'Tonne'),
        ('ton', 'Ton'),
        ('kWh', 'Kilowatt-heure'),
        ('Wh', 'Watt-heure'),
        ('other', 'Autre')
    ]
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()  # Utilisation de PositiveIntegerField pour garantir une valeur positive
    unit_of_measure = models.CharField(max_length=10, choices=UNIT_OF_MEASURE_CHOICES, default='unit')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='CDF')
    # exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.00)
    date = models.DateTimeField(auto_now_add=True) 
    tva_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.16)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_with_tva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    photo =  models.ImageField(
        upload_to="img/transactions/",
        blank=True,
        null=True,
    )
    
    objects = TransactionQuerySet.as_manager()
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['date']

    def __str__(self):
        return f"{self.product} - {self.id} - {self.date}"

    def clean(self):
        if self.type == 'sale':
            self.supplier = None  # Forcer supplier à null pour les transactions de type 'vente'
            if self.client is None:
                raise ValidationError(_("Le client doit être spécifié pour les transactions de vente."))
        elif self.type == 'purchase':
            self.client = None  # Forcer client à null pour les transactions de type 'achat'
            if self.supplier is None:
                raise ValidationError(_("Le fournisseur doit être spécifié pour les transactions d'achat."))

        producer_products = self.producer.product.all() if self.producer else []
        if self.product not in producer_products:
            raise ValidationError(_("Le produit n'est pas répertorié dans le profil du producteur."))

        if self.quantity <= 0:
            raise ValidationError(_("La quantité doit être un entier positif."))

        if self.price <= 0:
            raise ValidationError(_("Le prix doit être une valeur positive."))
    
    def save(self, *args, **kwargs):
        self.clean()  # Appeler clean pour vérifier les validations
        new_amount = self.price * self.quantity
        new_amount_with_tva = new_amount + (new_amount * self.tva_rate)
        is_new = self.pk is None

        if not is_new:
            previous = Transaction.objects.get(pk=self.pk)
            previous_amount_with_tva = previous.amount_with_tva

            if self.type == 'purchase':
                self.producer.current_balance += previous_amount_with_tva
                if previous.supplier:
                    previous.supplier.total_purchases -= previous_amount_with_tva
                    previous.supplier.save()
            elif self.type == 'sale':
                self.producer.current_balance -= previous_amount_with_tva
                if previous.client:
                    previous.client.total_sales -= previous_amount_with_tva
                    previous.client.save()

        self.amount = new_amount
        self.amount_with_tva = new_amount_with_tva

        if is_new:
            if self.type == 'purchase':
                if self.producer.current_balance < self.amount_with_tva:
                    raise ValidationError(_("Solde insuffisant pour cet achat."))
                self.producer.current_balance -= self.amount_with_tva
                if self.supplier:
                    self.supplier.total_purchases += self.amount_with_tva
                    self.supplier.save()
            elif self.type == 'sale':
                self.producer.current_balance += self.amount_with_tva
                if self.client:
                    self.client.total_sales += self.amount_with_tva
                    self.client.save()
        
        if self.photo:
            # Ouvrir l'image avec Pillow
            image = Image.open(self.photo)
            output = BytesIO()
            
            # Redimensionner l'image si nécessaire
            image = image.resize((800, 800))  # Par exemple, redimensionner à 800x800 pixels
            
            # Sauvegarder l'image dans le format souhaité
            image.save(output, format='JPEG', quality=85)
            output.seek(0)
            
            # Créer un nouveau fichier ContentFile
            self.photo.save(self.photo.name, ContentFile(output.getvalue()), save=False)

        super().save(*args, **kwargs)

        if not is_new:
            self.update_balances()

    def update_balances(self):
        if not self.pk:
            return

        previous = Transaction.objects.get(pk=self.pk)
        previous_amount_with_tva = previous.amount_with_tva

        if self.type == 'purchase':
            if self.producer.current_balance < self.amount_with_tva:
                raise ValidationError(_("Solde insuffisant pour cet achat."))
            self.producer.current_balance -= self.amount_with_tva
            if self.supplier:
                self.supplier.total_purchases += self.amount_with_tva
                self.supplier.save()
        elif self.type == 'sale':
            self.producer.current_balance += self.amount_with_tva
            if self.client:
                self.client.total_sales += self.amount_with_tva
                self.client.save()

        self.producer.save()

    def delete(self, *args, **kwargs):
        amount_with_tva = self.amount_with_tva

        if self.type == 'purchase':
            self.producer.current_balance += amount_with_tva
            if self.supplier:
                self.supplier.total_purchases -= amount_with_tva
                self.supplier.save()
        elif self.type == 'sale':
            self.producer.current_balance -= amount_with_tva
            if self.client:
                self.client.total_sales -= amount_with_tva
                self.client.save()

        self.producer.save()
        super().delete(*args, **kwargs)

    @staticmethod
    def total_purchases():
        purchases = Transaction.objects.filter(type='purchase').aggregate(total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())))
        return purchases['total'] if purchases['total'] else 0

    @staticmethod
    def total_sales():
        sales = Transaction.objects.filter(type='sale').aggregate(total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())))
        return sales['total'] if sales['total'] else 0

    @staticmethod
    def general_margin():
        total_purchases = Transaction.total_purchases()
        total_sales = Transaction.total_sales()
        margin = total_sales - total_purchases
        return margin
    
    @property
    def total_price(self):
        return self.price * self.quantity

    @property
    def total_price_cdf(self):
        if self.currency == 'USD':
            return self.total_price * 2842.12  # Taux de change USD -> CDF
        elif self.currency == 'EUR':
            return self.total_price * 3076.69  # Taux de change EUR -> CDF
        else:
            return self.total_price  # Si la devise est déjà CDF, retourner le prix tel quel
    
    @property
    def producer_province(self):
        return self.producer.province.name if self.producer and self.producer.province else None

    @property
    def supplier_province(self):
        return self.supplier.province.name if self.supplier and self.supplier.province else None

    @property
    def client_province(self):
        return self.client.province.name if self.client and self.client.province else None
    
    
    @classmethod
    def total_quantity_sales(cls):
        return cls.objects.filter(type='sale').aggregate(total=Sum('quantity'))['total'] or 0

    @classmethod
    def total_quantity_purchases(cls):
        return cls.objects.filter(type='purchase').aggregate(total=Sum('quantity'))['total'] or 0
    
    def get_details(self):
        details = {
            'producer': self.producer.company_name if self.producer else None,
            'product': self.product.product_label if self.product else None,
            'transaction_type': self.get_type_display(),
            'price': str(self.price),
            'quantity': self.quantity,
            'unit_of_measure': self.get_unit_of_measure_display(),
            'currency': self.get_currency_display(),
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'producer_province': self.producer_province,
            'supplier_province': self.supplier_province,
            'client_province': self.client_province,
            'total_price_cdf': str(self.total_price_cdf),
            'id': self.id,
        }
        if self.type == 'sale':
            details['client'] = self.client.name if self.client else None
        elif self.type == 'purchase':
            details['supplier'] = self.supplier.name if self.supplier else None
        return details

# Signal pour créer automatiquement un producteur pour chaque nouvel utilisateur
@receiver(post_save, sender=CustomUser)
def create_producer(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Producer.objects.create(user=instance, company_name=f"{instance.username}'s Company", email=instance.email, country_id=20, province_id=10)

@receiver(post_save, sender=Transaction)
@receiver(post_delete, sender=Transaction)
def update_client_total_sales(sender, instance, **kwargs):
    if instance.client:
        instance.client.update_total_sales()

@receiver(post_save, sender=Transaction)
@receiver(post_delete, sender=Transaction)
def update_supplier_total_purchases(sender, instance, **kwargs):
    if instance.supplier:
        instance.supplier.update_total_purchases()