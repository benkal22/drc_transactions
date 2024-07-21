# transactions/filters.py

import django_filters
from django import forms
from django_filters import DateFilter
from .models import Transaction, Product, Producer, Province, Supplier, UniqueSector, Country, Client

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['product_label']

class TransactionFilter(django_filters.FilterSet):
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        label='Choisir le produit',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    producer = django_filters.ModelChoiceFilter(
        queryset=Producer.objects.all(),
        label='Choisir le producteur',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        label='Type de transaction',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    date = DateFilter(
        field_name='date',
        lookup_expr='icontains',
        label='Date de la transaction',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    producer_province = django_filters.ModelChoiceFilter(
        queryset=Province.objects.all(),
        label='Province du producteur',
        method='filter_by_producer_province',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    supplier_province = django_filters.ModelChoiceFilter(
        queryset=Province.objects.all(),
        label='Province du fournisseur',
        method='filter_by_supplier_province',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    client_province = django_filters.ModelChoiceFilter(
        queryset=Province.objects.all(),
        label='Province du client',
        method='filter_by_client_province',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )

    class Meta:
        model = Transaction
        fields = ['product', 'producer', 'type', 'date', 'producer_province', 'supplier_province', 'client_province']

    def filter_by_producer_province(self, queryset, name, value):
        return queryset.filter(producer__province=value)

    def filter_by_supplier_province(self, queryset, name, value):
        return queryset.filter(supplier__province=value)

    def filter_by_client_province(self, queryset, name, value):
        return queryset.filter(client__province=value)

class ProducerFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(
        field_name='company_name',
        lookup_expr='icontains',
        label='Nom de la compagnie',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    manager_name = django_filters.CharFilter(
        field_name='manager_name',
        lookup_expr='icontains',
        label='Nom du gestionnaire',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    tax_code = django_filters.CharFilter(
        field_name='tax_code',
        lookup_expr='icontains',
        label='Code fiscal',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    nrc = django_filters.CharFilter(
        field_name='nrc',
        lookup_expr='icontains',
        label='NRC',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    nat_id = django_filters.CharFilter(
        field_name='nat_id',
        lookup_expr='icontains',
        label='Identifiant national',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    product = django_filters.ModelMultipleChoiceFilter(
        queryset=Product.objects.all(),
        label='Produits',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-multiselect block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    sector_label = django_filters.ModelChoiceFilter(
        queryset=UniqueSector.objects.all(),
        label='Secteur',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    phone_number = django_filters.CharFilter(
        field_name='phone_number',
        lookup_expr='icontains',
        label='Numéro de téléphone',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    country = django_filters.ModelChoiceFilter(
        queryset=Country.objects.filter(country='Congo (Kinshasa)'),
        label='Pays',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    province = django_filters.ModelChoiceFilter(
        queryset=Province.objects.all(),
        label='Province',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    is_approved = django_filters.BooleanFilter(
        field_name='is_approved',
        label='Approuvé',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    current_balance = django_filters.RangeFilter(
        field_name='current_balance',
        label='Solde',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current_balance'
        })
    )

    class Meta:
        model = Producer
        fields = [
            'company_name', 'manager_name', 'tax_code', 'nrc', 'nat_id', 'product', 
            'sector_label', 'email', 'phone_number', 'country', 'province', 
            'is_approved', 'initial_balance', 'current_balance'
        ]

class SupplierFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(
        choices=Supplier.CATEGORY_CHOICES,
        label='Catégorie',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Nom',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    manager_name = django_filters.CharFilter(
        field_name='manager_name',
        lookup_expr='icontains',
        label='Nom du gestionnaire',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    tax_code = django_filters.CharFilter(
        field_name='tax_code',
        lookup_expr='icontains',
        label='Code fiscal',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    nrc = django_filters.CharFilter(
        field_name='nrc',
        lookup_expr='icontains',
        label='NRC',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    nat_id = django_filters.CharFilter(
        field_name='nat_id',
        lookup_expr='icontains',
        label='Identifiant national',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    product = django_filters.ModelMultipleChoiceFilter(
        queryset=Product.objects.all(),
        label='Produits',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-multiselect block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    sector_label = django_filters.ModelMultipleChoiceFilter(
        queryset=UniqueSector.objects.all(),
        label='Secteurs',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-multiselect block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    phone_number = django_filters.CharFilter(
        field_name='phone_number',
        lookup_expr='icontains',
        label='Numéro de téléphone',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    country = django_filters.ModelChoiceFilter(
        queryset=Country.objects.all(),
        label='Pays',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    province = django_filters.ModelChoiceFilter(
        queryset=Province.objects.all(),
        label='Province',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    total_purchases = django_filters.RangeFilter(
        field_name='total_purchases',
        label='Total des achats',
        widget=forms.NumberInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )

    class Meta:
        model = Supplier
        fields = [
            'category', 'name', 'manager_name', 'tax_code', 'nrc', 'nat_id', 'product',
            'sector_label', 'email', 'phone_number', 'country', 'province', 'total_purchases'
        ]

class ClientFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(
        choices=Client.CATEGORY_CHOICES,
        label='Catégorie',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Nom',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    manager_name = django_filters.CharFilter(
        field_name='manager_name',
        lookup_expr='icontains',
        label='Nom du gestionnaire',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    tax_code = django_filters.CharFilter(
        field_name='tax_code',
        lookup_expr='icontains',
        label='Code fiscal',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    nrc = django_filters.CharFilter(
        field_name='nrc',
        lookup_expr='icontains',
        label='NRC',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    nat_id = django_filters.CharFilter(
        field_name='nat_id',
        lookup_expr='icontains',
        label='Identifiant national',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    product = django_filters.ModelMultipleChoiceFilter(
        queryset=Product.objects.all(),
        label='Produits',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-multiselect block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    sector_label = django_filters.ModelMultipleChoiceFilter(
        queryset=UniqueSector.objects.all(),
        label='Secteurs',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-multiselect block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    phone_number = django_filters.CharFilter(
        field_name='phone_number',
        lookup_expr='icontains',
        label='Numéro de téléphone',
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    country = django_filters.ModelChoiceFilter(
        queryset=Country.objects.all(),
        label='Pays',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    province = django_filters.ModelChoiceFilter(
        queryset=Province.objects.all(),
        label='Province',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    total_sales = django_filters.RangeFilter(
        field_name='total_sales',
        label='Total des ventes',
        widget=forms.NumberInput(attrs={
            'class': 'form-input block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )

    class Meta:
        model = Client
        fields = [
            'category', 'name', 'manager_name', 'tax_code', 'nrc', 'nat_id', 'product',
            'sector_label', 'email', 'phone_number', 'country', 'province', 'total_sales'
        ]
