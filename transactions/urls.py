#DRC_TRANSACTIONS/transactions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from transactions.views.clients_view import ClientViewSet, ClientListAPIView
from transactions.views.provinces_view import ProvinceViewSet
from transactions.views.products_view import ProductViewSet
from transactions.views.producers_view import ProducerViewSet
from transactions.views.suppliers_view import SupplierViewSet
from transactions.views.countries_view import CountryViewSet
from transactions.views.stocks_view import StockViewSet
from transactions.views.transactions_view import TransactionViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'provinces', ProvinceViewSet)
router.register(r'products', ProductViewSet)
router.register(r'producers', ProducerViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'stocks', StockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

