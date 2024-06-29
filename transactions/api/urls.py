#DRC_TRANSACTIONS/transactions/api/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from transactions.api.views import (
    CustomUserViewSet,
    ProducerViewSet,
    SupplierViewSet,
    ClientViewSet,
    TransactionViewSet,
    ProductViewSet,
    UniqueSectorViewSet,
    CountryViewSet,
    ProvinceViewSet,
)

router = DefaultRouter()
router.register(r'producers', ProducerViewSet, basename='producers')
router.register(r'clients', ClientViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'products', ProductViewSet)
router.register(r'unique-sectors', UniqueSectorViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'provinces', ProvinceViewSet)
router.register(r'custom-users', CustomUserViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
