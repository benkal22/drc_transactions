from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from ..models import (Producer, Client, Supplier, Transaction, Stock, Product, UniqueProduct, 
                      CustomUser, Country, Province)
from .serializers import (CustomUserSerializer, ProducerSerializer, ClientSerializer, SupplierSerializer, TransactionSerializer,
                          StockSerializer, ProductSerializer, UniqueProductSerializer, CountrySerializer, ProvinceSerializer)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
class UniqueProductViewSet(viewsets.ModelViewSet):
    queryset = UniqueProduct.objects.all()
    serializer_class = UniqueProductSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UniqueProduct.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Producer.objects.filter(user=self.request.user)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(client__user=self.request.user) | Transaction.objects.filter(supplier__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def total_sales(self, request):
        total = Transaction.objects.filter(type='sale').aggregate(total_sales=Sum('price'))
        return Response(total, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def total_purchases(self, request):
        total = Transaction.objects.filter(type='purchase').aggregate(total_purchases=Sum('price'))
        return Response(total, status=status.HTTP_200_OK)

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Stock.objects.filter(transaction__client__user=self.request.user) | Stock.objects.filter(transaction__supplier__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def total_stock(self, request):
        total = Stock.objects.aggregate(total_stock=Sum('total_quantity'))
        return Response(total, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def net_stock(self, request):
        net_stock = Stock.objects.aggregate(net_stock=Sum('net_stock_quantity'))
        return Response(net_stock, status=status.HTTP_200_OK)
