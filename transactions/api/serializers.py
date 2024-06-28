from rest_framework import serializers
from django.contrib.auth import get_user_model

from ..models import CustomUser, Producer, Product, UniqueSector, Country, Province, Transaction, Client, Supplier

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProducerSerializer(serializers.ModelSerializer):
    sector_label = serializers.StringRelatedField()  # Utilisation de StringRelatedField pour afficher le champ lisible
    product = serializers.StringRelatedField(many=True)  # Utilisation de StringRelatedField pour afficher les produits
    country = serializers.StringRelatedField()  # Utilisation de StringRelatedField pour afficher le pays
    province = serializers.StringRelatedField()  # Utilisation de StringRelatedField pour afficher la province

    class Meta:
        model = Producer
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    sector_label = serializers.StringRelatedField(many=True)
    product = serializers.StringRelatedField(many=True)
    country = serializers.StringRelatedField()
    province = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    sector_label = serializers.StringRelatedField(many=True)
    product = serializers.StringRelatedField(many=True)
    country = serializers.StringRelatedField()
    province = serializers.StringRelatedField()

    class Meta:
        model = Supplier
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField()
    client = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    sector_label = serializers.StringRelatedField()

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