from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, F
from ..models import ( 
    CustomUser, 
    Producer, 
    Client, 
    Supplier, 
    Transaction, 
    # Stock, 
    Product, 
    UniqueSector,
    Country
)
from .serializers import (
    CustomUserSerializer,
    ProducerSerializer,
    ClientSerializer,
    SupplierSerializer,
    TransactionSerializer,
    # StockSerializer,
    ProductSerializer,
    UniqueSectorSerializer,
    CountrySerializer
)

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
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from ..models import Producer, Supplier, Client

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

    @action(detail=False, methods=['get'])
    def transaction_count(self, request):
        # Nombre total de transactions effectuées par le producteur connecté
        transaction_count = Transaction.objects.filter(supplier__user=request.user).count()
        return Response({'transaction_count': transaction_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def supplier_count(self, request):
        # Nombre total de fournisseurs du producteur connecté
        supplier_count = Supplier.objects.filter(user=request.user).count()
        return Response({'supplier_count': supplier_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def enterprise_supplier_count(self, request):
        # Nombre de fournisseurs de type enterprise du producteur connecté
        enterprise_supplier_count = Supplier.objects.filter(user=request.user, category='enterprise').count()
        return Response({'enterprise_supplier_count': enterprise_supplier_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def individual_supplier_count(self, request):
        # Nombre de fournisseurs de type individual du producteur connecté
        individual_supplier_count = Supplier.objects.filter(user=request.user, category='individual').count()
        return Response({'individual_supplier_count': individual_supplier_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def client_count(self, request):
        # Nombre total de clients du producteur connecté
        client_count = Client.objects.filter(country__country='Congo (Kinshasa)').count()
        return Response({'client_count': client_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def enterprise_client_count(self, request):
        # Nombre de clients de type enterprise du producteur connecté
        enterprise_client_count = Client.objects.filter(category='enterprise', country__country='Congo (Kinshasa)').count()
        return Response({'enterprise_client_count': enterprise_client_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def individual_client_count(self, request):
        # Nombre de clients de type individual du producteur connecté
        individual_client_count = Client.objects.filter(category='individual', country__country='Congo (Kinshasa)').count()
        return Response({'individual_client_count': individual_client_count}, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        # Obtenir le résumé des ventes
        sales_summary = Transaction.objects.filter(type='sale').aggregate(
            total_sales=Sum('price'),
            total_quantity=Sum('quantity'),
            total_value=Sum('total_price')
        )
        return Response(sales_summary, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def purchase_summary(self, request):
        # Obtenir le résumé des achats
        purchase_summary = Transaction.objects.filter(type='purchase').aggregate(
            total_purchases=Sum('price'),
            total_quantity=Sum('quantity'),
            total_value=Sum('total_price')
        )
        return Response(purchase_summary, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def product_sales_ranking(self, request):
        # Classement des produits par ventes
        product_sales_ranking = Transaction.objects.filter(type='sale').values('product').annotate(
            total_sales=Sum('price'),
            total_quantity=Sum('quantity')
        ).order_by('-total_sales')
        return Response(product_sales_ranking, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def product_purchase_ranking(self, request):
        # Classement des produits par achats
        product_purchase_ranking = Transaction.objects.filter(type='purchase').values('product').annotate(
            total_purchases=Sum('price'),
            total_quantity=Sum('quantity')
        ).order_by('-total_purchases')
        return Response(product_purchase_ranking, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def client_sales_distribution(self, request):
        # Distribution des ventes par client
        client_sales_distribution = Transaction.objects.filter(type='sale').values('client').annotate(
            total_sales=Sum('price'),
            total_quantity=Sum('quantity')
        ).order_by('-total_sales')
        return Response(client_sales_distribution, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def supplier_purchase_distribution(self, request):
        # Distribution des achats par fournisseur
        supplier_purchase_distribution = Transaction.objects.filter(type='purchase').values('supplier').annotate(
            total_purchases=Sum('price'),
            total_quantity=Sum('quantity')
        ).order_by('-total_purchases')
        return Response(supplier_purchase_distribution, status=status.HTTP_200_OK)

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
