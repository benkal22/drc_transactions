from django.urls import include, path
from rest_framework.routers import DefaultRouter
from transactions.api.views import (
    CustomUserViewSet, ProducerViewSet, SupplierViewSet,
    ClientViewSet, TransactionViewSet, ProductViewSet,
    UniqueSectorViewSet, CountryViewSet, ProvinceViewSet
)

router = DefaultRouter()
router.register(r'producers', ProducerViewSet, basename='producers')
router.register(r'clients', ClientViewSet)
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'unique-sectors', UniqueSectorViewSet, basename='unique-sectors')
router.register(r'countries', CountryViewSet, basename='countries')
router.register(r'provinces', ProvinceViewSet, basename='provinces')
router.register(r'custom-users', CustomUserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),  # Inclusion des routes du routeur
]
