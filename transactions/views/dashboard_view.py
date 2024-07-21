# DRC_TRANSACTIONS/views.py

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from ..models import Transaction, Product, Producer, Supplier, Client, Province, Country, UniqueSector, ProducerClient, ProducerSupplier
import pandas as pd
from collections import defaultdict
from django.views.generic import ListView
from transactions.filters import TransactionFilter

from django_filters.views import FilterView
from django.db.models import Sum, Count, F, Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.views import APIView
from transactions.serializers import CorrelationMatrixSerializer, CorrelationMatrixStatisticsSerializer
from transactions.forms import ProductMatrixFilterForm

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.generic import TemplateView
import json
from decimal import Decimal

def decimal_to_float(d):
    if isinstance(d, list):
        return [decimal_to_float(i) for i in d]
    if isinstance(d, dict):
        return {k: decimal_to_float(v) for k, v in d.items()}
    if isinstance(d, Decimal):
        return float(d)
    return d

class TransactionMixin:
    def get_transaction_context(self):
        transactions = Transaction.objects.all()
        total_transactions = transactions.count()
        total_purchases = transactions.filter(type='purchase').count()
        total_sales = transactions.filter(type='sale').count()
        
        total_revenue_cdf = sum(t.total_price_cdf for t in transactions)
        total_purchase_price_cdf = sum(t.total_price_cdf for t in transactions if t.type == 'purchase')
        total_sales_price_cdf = sum(t.total_price_cdf for t in transactions if t.type == 'sale')
        total_margin_cdf = total_sales_price_cdf - total_purchase_price_cdf

        producer_provinces = transactions.values_list('producer__province__name', flat=True).distinct()
        supplier_provinces = transactions.filter(type='purchase').values_list('supplier__province__name', flat=True).distinct()
        client_provinces = transactions.filter(type='sale').values_list('client__province__name', flat=True).distinct()
        
        return {
            'total_transactions': total_transactions,
            'total_purchases': total_purchases,
            'total_sales': total_sales,
            'total_revenue_cdf': total_revenue_cdf,
            'total_purchase_price_cdf': total_purchase_price_cdf,
            'total_sales_price_cdf': total_sales_price_cdf,
            'total_margin_cdf': total_margin_cdf,
            'producer_provinces': producer_provinces,
            'supplier_provinces': supplier_provinces,
            'client_provinces': client_provinces,
        }

class ChartMixin:
    def get_chart_context(self):
        transactions = Transaction.objects.all()
        purchases = [t for t in transactions if t.type == 'purchase']
        sales = [t for t in transactions if t.type == 'sale']
        margins = [
            sale.total_price_cdf - purchase.total_price_cdf 
            for sale in sales for purchase in purchases 
            if sale.product == purchase.product and sale.date > purchase.date
        ]
        
        purchases_data = {
            'dates': [t.date.strftime('%Y-%m-%d') for t in purchases],
            'amounts': [float(t.total_price_cdf) for t in purchases]
        }
        
        sales_data = {
            'dates': [t.date.strftime('%Y-%m-%d') for t in sales],
            'amounts': [float(t.total_price_cdf) for t in sales]
        }
        
        margins_data = {
            'dates': list(range(len(margins))),
            'amounts': [float(m) for m in margins]
        }

        return {
            'purchases_data': json.dumps(purchases_data),
            'sales_data': json.dumps(sales_data),
            'margins_data': json.dumps(margins_data),
        }
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json

class DashboardListView(TransactionMixin, ChartMixin, FilterView, ListView):
    model = Transaction
    template_name = 'transactions/reports/reports.html'
    context_object_name = 'transactions'
    filterset_class = TransactionFilter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()
        transaction_details = json.dumps([transaction.get_details() for transaction in transactions], cls=DjangoJSONEncoder)
        context['transaction_details_json'] = mark_safe(transaction_details)
        context.update(self.get_transaction_context())
        # context.update(self.get_chart_context())
        return context

    
def reports_provinces(request):
    # Filtrage initial des transactions de type achat entre producteurs et fournisseurs
    transactions = Transaction.objects.filter(
        type='purchase',
        supplier__isnull=False
    ).select_related('producer', 'product', 'producer__province', 'producer__sector_label')

    # Récupération des options de filtrage pour les provinces, produits et secteurs uniques
    provinces = Province.objects.all()
    products = Product.objects.all()
    unique_sectors = UniqueSector.objects.all()

    # Filtrage supplémentaire par province, produit et secteur unique si les paramètres sont présents dans la requête GET
    province_filter = request.GET.get('province')
    product_filter = request.GET.get('product')
    sector_filter = request.GET.get('sector')

    if province_filter:
        transactions = transactions.filter(producer__province__name=province_filter)
    if product_filter:
        transactions = transactions.filter(product__product_label=product_filter)
    if sector_filter:
        transactions = transactions.filter(producer__sector_label__sector_label=sector_filter)

    # Agrégation des données pour obtenir la somme des quantités et des prix totaux
    transaction_summary = transactions.values(
        'producer__province__name',
        'product__product_label',
        'producer__sector_label__sector_label'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_price=Sum('price')
    ).order_by('producer__province__name')

    # Pagination des résultats
    paginator = Paginator(transaction_summary, 10)  # 10 éléments par page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'provinces': provinces,
        'products': products,
        'unique_sectors': unique_sectors,
    }

    return render(request, 'transactions/reports/provinces.html', context)

class CorrelationMatrixAPIView(APIView):

    def get(self, request):
        # Récupération des données du formulaire de filtre (s'il y en a)
        product = request.GET.get('product')
        matrix_type = request.GET.get('matrix_type', 'quantity')

        # Sélection des transactions en utilisant select_related pour éviter les requêtes multiples
        transactions = Transaction.objects.select_related('producer__province', 'supplier__province', 'client__province').all()

        if product:
            transactions = transactions.filter(product=product)

        data_producer_supplier = []
        data_producer_client = []

        total_quantity_purchased = 0
        total_quantity_sold = 0
        total_quantity_imported = 0
        total_quantity_exported = 0
        total_price_purchased = 0
        total_price_sold = 0

        for transaction in transactions:
            producer_province = transaction.producer.province.name
            if transaction.type == 'purchase' and transaction.supplier:
                other_province = transaction.supplier.province.name
                total_price = transaction.price * transaction.quantity
                data_producer_supplier.append({
                    'Producer_Province': producer_province,
                    'Other_Province': other_province,
                    'Quantity': transaction.quantity,
                    'Total_Price': total_price
                })
                total_quantity_purchased += transaction.quantity
                total_price_purchased += total_price
                if transaction.supplier.country.country != 'Congo (Kinshasa)':
                    total_quantity_imported += transaction.quantity
            elif transaction.type == 'sale' and transaction.client:
                other_province = transaction.client.province.name
                total_price = transaction.price * transaction.quantity
                data_producer_client.append({
                    'Producer_Province': producer_province,
                    'Other_Province': other_province,
                    'Quantity': transaction.quantity,
                    'Total_Price': total_price
                })
                total_quantity_sold += transaction.quantity
                total_price_sold += total_price
                if transaction.client.country.country != 'Congo (Kinshasa)':
                    total_quantity_exported += transaction.quantity

        df_producer_supplier = pd.DataFrame(data_producer_supplier)
        df_producer_client = pd.DataFrame(data_producer_client)

        provinces = list(Province.objects.values_list('name', flat=True).distinct())

        correlation_matrix_producer_supplier = pd.DataFrame(index=provinces, columns=provinces)
        correlation_matrix_producer_client = pd.DataFrame(index=provinces, columns=provinces)

        value_column = 'Total_Price' if matrix_type == 'price' else 'Quantity'

        for index, row in df_producer_supplier.iterrows():
            producer_province = row['Producer_Province']
            other_province = row['Other_Province']
            value = row[value_column]

            correlation_matrix_producer_supplier.loc[producer_province, other_province] = value
            correlation_matrix_producer_supplier.loc[other_province, producer_province] = value

        for index, row in df_producer_client.iterrows():
            producer_province = row['Producer_Province']
            other_province = row['Other_Province']
            value = row[value_column]

            correlation_matrix_producer_client.loc[producer_province, other_province] = value
            correlation_matrix_producer_client.loc[other_province, producer_province] = value

        correlation_matrix_producer_supplier.fillna(0, inplace=True)
        correlation_matrix_producer_client.fillna(0, inplace=True)

        # Conversion en listes JSON pour l'envoi
        correlation_matrix_producer_supplier_json = correlation_matrix_producer_supplier.reset_index().rename(columns={'index': 'Producer_Province'}).to_dict(orient='records')
        correlation_matrix_producer_client_json = correlation_matrix_producer_client.reset_index().rename(columns={'index': 'Producer_Province'}).to_dict(orient='records')

        data = {
            'correlation_matrix_producer_supplier': correlation_matrix_producer_supplier_json,
            'correlation_matrix_producer_client': correlation_matrix_producer_client_json,
            'total_quantity_purchased': total_quantity_purchased,
            'total_quantity_sold': total_quantity_sold,
            'total_quantity_imported': total_quantity_imported,
            'total_quantity_exported': total_quantity_exported,
            'total_price_purchased': total_price_purchased,
            'total_price_sold': total_price_sold,
            'provinces': provinces,
        }

        return Response(data)

from django.shortcuts import render
from django.views import View
from decimal import Decimal
from ..filters import TransactionFilter
import json

class CorrelationMatrixView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        filter = TransactionFilter(request.GET, queryset=Transaction.objects.all())
        transactions = filter.qs

        sales_matrix, sales_provinces = self.get_sales_matrix(transactions)
        purchase_matrix, purchase_provinces = self.get_purchase_matrix(transactions)

        data = {
            'products': list(products.values('id', 'product_label')),
            'sales_matrix': self.convert_decimal_to_float(sales_matrix),
            'purchase_matrix': self.convert_decimal_to_float(purchase_matrix),
            'sales_provinces': sales_provinces,
            'purchase_provinces': purchase_provinces,
            'sales_heatmap_data': self.convert_matrix_to_heatmap_data(sales_matrix, sales_provinces),
            'purchase_heatmap_data': self.convert_matrix_to_heatmap_data(purchase_matrix, purchase_provinces),
        }

        context = {
            'filter': filter,
            'data_json': json.dumps(data),  # Convertir les données en JSON pour le template
        }

        return render(request, 'transactions/reports/matrix.html', context)

    def get_sales_matrix(self, transactions):
        sales = transactions.filter(type='sale')
        matrix = {}
        provinces = set()
        for sale in sales:
            producer_province = sale.producer_province
            client_province = sale.client_province
            if producer_province not in matrix:
                matrix[producer_province] = {}
            if client_province not in matrix[producer_province]:
                matrix[producer_province][client_province] = {'quantity': 0, 'total_price': Decimal('0.0')}
            matrix[producer_province][client_province]['quantity'] += sale.quantity
            matrix[producer_province][client_province]['total_price'] += sale.total_price
            provinces.add(producer_province)
            provinces.add(client_province)
        return matrix, sorted(provinces)

    def get_purchase_matrix(self, transactions):
        purchases = transactions.filter(type='purchase')
        matrix = {}
        provinces = set()
        for purchase in purchases:
            producer_province = purchase.producer_province
            supplier_province = purchase.supplier_province
            if producer_province not in matrix:
                matrix[producer_province] = {}
            if supplier_province not in matrix[producer_province]:
                matrix[producer_province][supplier_province] = {'quantity': 0, 'total_price': Decimal('0.0')}
            matrix[producer_province][supplier_province]['quantity'] += purchase.quantity
            matrix[producer_province][supplier_province]['total_price'] += purchase.total_price
            provinces.add(producer_province)
            provinces.add(supplier_province)
        return matrix, sorted(provinces)

    def convert_decimal_to_float(self, matrix):
        for producer_province in matrix:
            for province in matrix[producer_province]:
                matrix[producer_province][province]['total_price'] = float(matrix[producer_province][province]['total_price'])
        return matrix

    def convert_matrix_to_heatmap_data(self, matrix, provinces):
        heatmap_data = []
        for producer_province in provinces:
            data = []
            for province in provinces:
                value = matrix.get(producer_province, {}).get(province, {'quantity': 0, 'total_price': 0})
                data.append({'x': province, 'y': value['total_price'], 'quantity': value['quantity']})
            heatmap_data.append({'name': producer_province, 'data': data})
        return heatmap_data

class EconomicsPredictionView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        filter = TransactionFilter(request.GET, queryset=Transaction.objects.all())
        transactions = filter.qs

        sales_matrix, sales_provinces = self.get_sales_matrix(transactions)
        purchase_matrix, purchase_provinces = self.get_purchase_matrix(transactions)

        data = {
            'products': list(products.values('id', 'product_label')),
            'sales_matrix': self.convert_decimal_to_float(sales_matrix),
            'purchase_matrix': self.convert_decimal_to_float(purchase_matrix),
            'sales_provinces': sales_provinces,
            'purchase_provinces': purchase_provinces,
            'sales_heatmap_data': self.convert_matrix_to_heatmap_data(sales_matrix, sales_provinces),
            'purchase_heatmap_data': self.convert_matrix_to_heatmap_data(purchase_matrix, purchase_provinces),
        }

        context = {
            'filter': filter,
            'data_json': json.dumps(data),  # Convertir les données en JSON pour le template
        }

        return render(request, 'transactions/reports/matrix.html', context)

    def get_sales_matrix(self, transactions):
        sales = transactions.filter(type='sale')
        matrix = {}
        provinces = set()
        for sale in sales:
            producer_province = sale.producer_province
            client_province = sale.client_province
            if producer_province not in matrix:
                matrix[producer_province] = {}
            if client_province not in matrix[producer_province]:
                matrix[producer_province][client_province] = {'quantity': 0, 'total_price': Decimal('0.0')}
            matrix[producer_province][client_province]['quantity'] += sale.quantity
            matrix[producer_province][client_province]['total_price'] += sale.total_price
            provinces.add(producer_province)
            provinces.add(client_province)
        return matrix, sorted(provinces)

    def get_purchase_matrix(self, transactions):
        purchases = transactions.filter(type='purchase')
        matrix = {}
        provinces = set()
        for purchase in purchases:
            producer_province = purchase.producer_province
            supplier_province = purchase.supplier_province
            if producer_province not in matrix:
                matrix[producer_province] = {}
            if supplier_province not in matrix[producer_province]:
                matrix[producer_province][supplier_province] = {'quantity': 0, 'total_price': Decimal('0.0')}
            matrix[producer_province][supplier_province]['quantity'] += purchase.quantity
            matrix[producer_province][supplier_province]['total_price'] += purchase.total_price
            provinces.add(producer_province)
            provinces.add(supplier_province)
        return matrix, sorted(provinces)

    def convert_decimal_to_float(self, matrix):
        for producer_province in matrix:
            for province in matrix[producer_province]:
                matrix[producer_province][province]['total_price'] = float(matrix[producer_province][province]['total_price'])
        return matrix

    def convert_matrix_to_heatmap_data(self, matrix, provinces):
        heatmap_data = []
        for producer_province in provinces:
            data = []
            for province in provinces:
                value = matrix.get(producer_province, {}).get(province, {'quantity': 0, 'total_price': 0})
                data.append({'x': province, 'y': value['total_price'], 'quantity': value['quantity']})
            heatmap_data.append({'name': producer_province, 'data': data})
        return heatmap_data

from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'transactions/reports/transaction_dashboard.html')

