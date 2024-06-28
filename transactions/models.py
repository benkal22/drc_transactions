# transactions/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

# Modèle personnalisé pour les utilisateurs
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Champ email unique
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()  # Utilisation du gestionnaire personnalisé

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

# Modèle pour les pays
class Country(models.Model):
    country = models.CharField(max_length=100)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['country']

    def __str__(self):
        return self.country

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
    id_product = models.AutoField(primary_key=True)
    sector_code = models.CharField(max_length=100)
    sector_label = models.CharField(max_length=255)
    activity_code = models.CharField(max_length=100)
    activity_label = models.CharField(max_length=255)
    product_code = models.CharField(max_length=100)
    product_label = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['product_label']

    def __str__(self):
        return self.product_label

    def __unicode__(self):
        return self.product_label

# Modèle pour les secteurs uniques
class UniqueSector(models.Model):
    sector_code = models.CharField(max_length=50)
    sector_label = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
        unique_together = ('sector_code', 'sector_label')
        ordering = ['sector_label']

    def __str__(self):
        return f"{self.sector_label} - {self.sector_code }"

# Modèle pour les producteurs
class Producer(models.Model):
    id_producer = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, editable=False)
    company_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    tax_code = models.CharField(max_length=100, blank=True, null=True)
    nrc = models.CharField(max_length=100, blank=True, null=True)
    nat_id = models.CharField(max_length=100, blank=True, null=True)
    product = models.ManyToManyField(Product)
    sector_label = models.ForeignKey(UniqueSector, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, default=1, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"

    def __unicode__(self):
        return self.company_name

    def __str__(self):
        return self.company_name

    def update_sector_labels(self):
        # Met à jour les étiquettes de secteur pour le producteur
        sector_labels = Product.objects.values_list('sector_label', flat=True).distinct()
        self.sector_label = ', '.join(sector_labels)
        self.save()

    @property
    def get_products_by_sector(self):
        # Retourne les produits du producteur par secteur
        return Product.objects.filter(sector_label=self.sector_label.sector_label)

# Modèle pour les clients
class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    CATEGORY_CHOICES = [
        ('enterprise', 'Enterprise'),
        ('individual', 'Individual')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    tax_code = models.CharField(max_length=100, blank=True, null=True)
    nrc = models.CharField(max_length=100, blank=True, null=True)
    nat_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    product = models.ManyToManyField(Product)
    sector_label = models.ManyToManyField(UniqueSector)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __unicode__(self):
        if self.category == 'enterprise':
            return self.company_name if self.company_name else "No company name"
        return self.name if self.name else "No name"

    def __str__(self):
        return self.__unicode__()

# Modèle pour les fournisseurs
class Supplier(models.Model):
    id_supplier = models.AutoField(primary_key=True)
    CATEGORY_CHOICES = [
        ('enterprise', 'Enterprise'),
        ('individual', 'Individual')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    tax_code = models.CharField(max_length=100, blank=True, null=True)
    nrc = models.CharField(max_length=100, blank=True, null=True)
    nat_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    product = models.ManyToManyField(Product)
    sector_label = models.ManyToManyField(UniqueSector)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __unicode__(self):
        if self.category == 'enterprise':
            return self.company_name if self.company_name else "No company name"
        return self.name if self.name else "No name"

    def __str__(self):
        return self.__unicode__()

# Modèle pour les transactions
class Transaction(models.Model):
    id_transaction = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    TRANSACTION_TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale')
    ]
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.product} - {self.id_transaction}"

    def clean(self):
        # Validation des transactions
        if self.type == 'sale' and self.client is None:
            raise ValidationError("Client must be specified for sales transactions.")
        if self.type == 'purchase' and self.supplier is None:
            raise ValidationError("Supplier must be specified for purchase transactions.")
        producer_products = self.supplier.product.all() if self.supplier else []
        if self.product not in producer_products:
            raise ValidationError("The product is not listed in the producer's profile.")

    @property
    def total_price(self):
        return self.price * self.quantity

# Signal pour créer automatiquement un producteur pour chaque nouvel utilisateur
@receiver(post_save, sender=CustomUser)
def create_producer(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Producer.objects.create(user=instance, company_name=f"{instance.username}'s Company", email=instance.email, country_id=20, province_id=10)
