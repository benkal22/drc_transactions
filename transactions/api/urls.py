from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'producers', views.ProducerViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'transactions', views.TransactionViewSet)
# router.register(r'stocks', views.StockViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'unique-products', views.UniqueSectorViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'custom-users', views.CustomUserViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
