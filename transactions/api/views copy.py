#DRC_TRANSACTIONS/transactions/api/views.py

from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, F

from ..models import CustomUser, Producer, Client, Supplier, Transaction, Product, UniqueSector, Country, Province
from .serializers import (
    CustomUserSerializer, ProducerSerializer, ClientSerializer, SupplierSerializer, TransactionSerializer,
    ProductSerializer, UniqueSectorSerializer, CountrySerializer, ProvinceSerializer
)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('product_label')
    serializer_class = ProductSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

class UniqueSectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UniqueSector.objects.all().order_by('sector_label')
    serializer_class = UniqueSectorSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class ProducerViewSet(viewsets.ModelViewSet):
    serializer_class = ProducerSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Producer.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Producer.objects.all()
        return Producer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        producer = self.get_object()
        transactions = Transaction.objects.filter(producer=producer)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(country__country='Congo (Kinshasa)')

class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Supplier.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Supplier.objects.all()
        return Supplier.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        producer = Producer.objects.filter(user=self.request.user).first()
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        elif producer:
            return Transaction.objects.filter(producer=producer)
        elif hasattr(self.request.user, 'supplier'):
            supplier = Supplier.objects.filter(user=self.request.user).first()
            return Transaction.objects.filter(supplier=supplier)
        elif hasattr(self.request.user, 'client'):
            client = Client.objects.filter(user=self.request.user).first()
            return Transaction.objects.filter(client=client)
        return Transaction.objects.none()

    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        sales_summary = Transaction.objects.filter(type='sale').aggregate(
            total_sales=Sum('price'),
            total_quantity=Sum('quantity'),
            total_value=Sum('price') * F('quantity')
        )
        return Response(sales_summary, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def purchase_summary(self, request):
        purchase_summary = Transaction.objects.filter(type='purchase').aggregate(
            total_purchases=Sum('price'),
            total_quantity=Sum('quantity'),
            total_value=Sum('price') * F('quantity')
        )
        return Response(purchase_summary, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def product_sales_ranking(self, request):
        product_sales_ranking = Transaction.objects.filter(type='sale').values('product').annotate(
            total_sales=Sum('price'),
            total_quantity=Sum('quantity')
        ).order_by('-total_sales')
        return Response(product_sales_ranking, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def product_purchase_ranking(self, request):
        product_purchase_ranking = Transaction.objects.filter(type='purchase').values('product').annotate(
            total_purchases=Sum('price'),
            total_quantity=Sum('quantity')
        ).order_by('-total_purchases')
        return Response(product_purchase_ranking, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def client_sales_distribution(self, request):
        client_sales_distribution = Transaction.objects.filter(type='sale').values('client').annotate(
            total_sales=Sum('price'),
            total_quantity=Sum('quantity')
        ).order_by('-total_sales')
        return Response(client_sales_distribution, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def supplier_purchase_distribution(self, request):
        supplier_purchase_distribution = Transaction.objects.filter(type='purchase').values('supplier').annotate(
            total_purchases=Sum('price'),
            total_quantity=Sum('quantity')
        ).order_by('-total_purchases')
        return Response(supplier_purchase_distribution, status=status.HTTP_200_OK)
