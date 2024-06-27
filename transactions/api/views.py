from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from ..models import CustomUser, Producer, Client, Supplier, Transaction, Stock, Product, UniqueProduct, Country
from .serializers import (
    CustomUserSerializer,
    ProducerSerializer,
    ClientSerializer,
    SupplierSerializer,
    TransactionSerializer,
    StockSerializer,
    ProductSerializer,
    UniqueProductSerializer,
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
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(client__country__country='Congo (Kinshasa)')

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def total_sales(self, request):
        total = Transaction.objects.filter(type='sale').aggregate(total_sales=Sum('price'))
        return Response(total, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def total_purchases(self, request):
        total = Transaction.objects.filter(type='purchase').aggregate(total_purchases=Sum('price'))
        return Response(total, status=status.HTTP_200_OK)


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StockSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Stock.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Stock.objects.all()
        return Stock.objects.filter(transaction__client__country__country='Congo (Kinshasa)')

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


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class UniqueProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UniqueProduct.objects.all()
    serializer_class = UniqueProductSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
