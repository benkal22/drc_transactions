from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import CustomUser, Country, Province, Product, UniqueProduct, Producer, Client, Supplier, Transaction, Stock

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country', 'iso2', 'iso3']

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'chef_lieu', 'superficie', 'population', 'rank']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id_product', 'sector_code', 'sector_label', 'activity_code', 'activity_label', 'product_code', 'product_label']

class UniqueProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniqueProduct
        fields = ['id', 'sector_code', 'sector_label', 'activity_code', 'activity_label']

class ProducerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), default=Country.objects.get(country='Congo (Kinshasa)').id)
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), required=False)

    class Meta:
        model = Producer
        fields = ['id_producer', 'user', 'company_name', 'manager_name', 'tax_code', 'nrc', 'nat_id', 'product', 'sector_label', 'photo', 'address', 'email', 'phone_number', 'country', 'province', 'is_approved']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.country.country != "Congo (Kinshasa)":
            representation.pop('province', None)
        return representation

    def validate(self, data):
        if data.get('country').country != "Congo (Kinshasa)" and 'province' in data:
            data.pop('province')
        return data

    def create(self, validated_data):
        products_data = validated_data.pop('product')
        producer = Producer.objects.create(**validated_data)
        for product_data in products_data:
            Product.objects.create(producer=producer, **product_data)
        return producer

    def update(self, instance, validated_data):
        products_data = validated_data.pop('product')
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.manager_name = validated_data.get('manager_name', instance.manager_name)
        instance.tax_code = validated_data.get('tax_code', instance.tax_code)
        instance.nrc = validated_data.get('nrc', instance.nrc)
        instance.nat_id = validated_data.get('nat_id', instance.nat_id)
        instance.address = validated_data.get('address', instance.address)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.country = validated_data.get('country', instance.country)
        instance.province = validated_data.get('province', instance.province) if validated_data.get('country').country == "Congo (Kinshasa)" else None
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()

        instance.product.clear()
        for product_data in products_data:
            instance.product.add(Product.objects.get(**product_data))
        
        return instance
    
class ClientSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    product = ProductSerializer(many=True, read_only=True)
    sector_label = UniqueProductSerializer(many=True)

    class Meta:
        model = Client
        fields = ['id_client', 'category', 'company_name', 'manager_name', 'tax_code', 'nrc', 'nat_id', 'name', 'product', 'sector_label', 'photo', 'address', 'email', 'phone_number', 'country', 'province']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products_count'] = instance.product.count()
        return representation

class SupplierSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    product = ProductSerializer(many=True, read_only=True)
    sector_label = UniqueProductSerializer(many=True)

    class Meta:
        model = Supplier
        fields = ['id_supplier', 'category', 'company_name', 'manager_name', 'tax_code', 'nrc', 'nat_id', 'name', 'product', 'sector_label', 'photo', 'address', 'email', 'phone_number', 'country', 'province']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products_count'] = instance.product.count()
        return representation

class TransactionSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id_transaction', 'type', 'supplier', 'client', 'price', 'quantity', 'date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_value'] = instance.price * instance.quantity
        return representation

class StockSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = ['id_stock', 'transaction', 'quantity_purchase', 'quantity_sale', 'total_quantity', 'net_stock_quantity', 'average_price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['transaction_details'] = TransactionSerializer(instance.transaction).data
        return representation
