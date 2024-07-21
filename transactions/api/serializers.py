#DRC_TRANSACTIONS/transactions/api/serializers.py

from rest_framework import serializers
from ..models import CustomUser, Producer, Product, UniqueSector, Country, Province, Transaction, Client, Supplier

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProducerSerializer(serializers.ModelSerializer):
    sector_label = serializers.StringRelatedField()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())

    class Meta:
        model = Producer
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    sector_label = serializers.PrimaryKeyRelatedField(queryset=UniqueSector.objects.all(), many=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())

    class Meta:
        model = Client
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    sector_label = serializers.PrimaryKeyRelatedField(queryset=UniqueSector.objects.all(), many=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())

    class Meta:
        model = Supplier
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), allow_null=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), allow_null=True)
    currency = serializers.ChoiceField(choices=Transaction.CURRENCY_CHOICES)
    exchange_rate = serializers.DecimalField(max_digits=10, decimal_places=4, default=1.00, read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    sector_label = serializers.PrimaryKeyRelatedField(queryset=UniqueSector.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

class UniqueSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniqueSector
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'
