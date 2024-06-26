# transactions/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

from django.db import models
from django.contrib.auth.models import AbstractUser

class Country(models.Model):
    country = models.CharField(max_length=100)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.country

# class Country(models.Model):
#     city = models.CharField(max_length=100)
#     city_ascii = models.CharField(max_length=100, blank=True)
#     city_alt = models.CharField(max_length=100, blank=True)
#     lat = models.FloatField()
#     lng = models.FloatField()
#     country = models.CharField(max_length=100)
#     iso2 = models.CharField(max_length=2)
#     iso3 = models.CharField(max_length=3)
#     admin_name = models.CharField(max_length=100, blank=True)
#     admin_name_ascii = models.CharField(max_length=100, blank=True)
#     admin_code = models.CharField(max_length=10, blank=True)
#     admin_type = models.CharField(max_length=50, blank=True)
#     capital = models.CharField(max_length=20, blank=True)
#     density = models.IntegerField()
#     population = models.IntegerField()
#     population_proper = models.IntegerField()
#     timezone = models.CharField(max_length=50)
#     ranking = models.IntegerField()
#     same_name = models.BooleanField()
#     id = models.BigIntegerField(primary_key=True)

#     class Meta:
#         verbose_name = "Country"
#         verbose_name_plural = "Countries"

#     def __str__(self):
#         return self.city

#     def __unicode__(self):
#         return self.city

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

class Producer(models.Model):
    id_producer = models.AutoField(primary_key=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    tax_code = models.CharField(max_length=100, blank=True, null=True)
    nrc = models.CharField(max_length=100, blank=True, null=True)
    nat_id = models.CharField(max_length=100, blank=True, null=True)
    product = models.ManyToManyField(Product)
    sector_label = models.CharField(max_length=255)
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