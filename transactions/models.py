# transactions/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Champ email unique
    
    # Définir le champ USERNAME_FIELD à 'username' et REQUIRED_FIELDS à ['email']
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()  # Utilisez le gestionnaire personnalisé

    def __str__(self):
        return self.username
    
    def __unicode__(self):
        return self.username
    
class Country(models.Model):
    country = models.CharField(max_length=100)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.country

class Province(models.Model):
    name = models.fields.CharField(max_length=150)
    chef_lieu = models.fields.CharField(null=True, max_length=150)
    superficie= models.fields.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    population = models.fields.IntegerField(blank=True, null=True) 
    rank =  models.fields.CharField(max_length=150, blank=True, null=True)
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.product_label

    def __unicode__(self):
        return self.product_label

class UniqueProduct(models.Model):
    sector_code = models.CharField(max_length=50)
    sector_label = models.CharField(max_length=100)
    activity_code = models.CharField(max_length=50)
    activity_label = models.CharField(max_length=100)

    class Meta:
        unique_together = ('sector_code', 'sector_label', 'activity_code', 'activity_label')

    def __str__(self):
        return f"{self.sector_label} - {self.activity_label}"

class Producer(models.Model):
    id_producer = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, editable=False)
    company_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    tax_code = models.CharField(max_length=100, blank=True, null=True)
    nrc = models.CharField(max_length=100, blank=True, null=True)
    nat_id = models.CharField(max_length=100, blank=True, null=True)
    product = models.ManyToManyField(Product)
    sector_label = models.ForeignKey(UniqueProduct, on_delete=models.CASCADE, null=True)
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

    def __str__(self):
        return self.company_name

    def __unicode__(self):
        return self.company_name
    
    def update_sector_labels(self):
        sector_labels = Product.objects.values_list('sector_label', flat=True).distinct()
        self.sector_label = ', '.join(sector_labels)
        self.save()
    
    @property
    def get_products_by_sector(self):
        return Product.objects.filter(sector_label=self.sector_label.sector_label)

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
    sector_label = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.company_name if self.category == 'enterprise' else self.name

    def __unicode__(self):
        return self.company_name if self.category == 'enterprise' else self.name

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
    sector_label = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.company_name if self.category == 'enterprise' else self.name

    def __unicode__(self):
        return self.company_name if self.category == 'enterprise' else self.name

class Transaction(models.Model):
    id_transaction = models.AutoField(primary_key=True)
    TRANSACTION_TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale')
    ]
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f'{self.type} - {self.date}'

    def __unicode__(self):
        return f'{self.type} - {self.date}'

class Stock(models.Model):
    id_stock = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    quantity_purchase = models.IntegerField()
    quantity_sale = models.IntegerField()
    total_quantity = models.IntegerField()
    net_stock_quantity = models.IntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f'Stock - {self.id_stock}'

    def __unicode__(self):
        return f'Stock - {self.id_stock}'
    
@receiver(post_save, sender=CustomUser)
def create_producer(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Producer.objects.create(user=instance, company_name=f"{instance.username}'s Company", email=instance.email, country_id=20, province_id=10)
    
        