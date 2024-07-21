from rest_framework import serializers
from .models import *

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CorrelationMatrixSerializer(serializers.Serializer):
    producer_province = serializers.CharField()
    other_province = serializers.CharField()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class CorrelationMatrixStatisticsSerializer(serializers.Serializer):
    total_quantity_purchased = serializers.IntegerField()
    total_quantity_sold = serializers.IntegerField()
    total_quantity_imported = serializers.IntegerField()
    total_quantity_exported = serializers.IntegerField()
    total_price_purchased = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price_sold = serializers.DecimalField(max_digits=10, decimal_places=2)
