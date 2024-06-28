"""
URL configuration for DRC_TRANSACTIONS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from transactions.views.producers_view import (
    producers_list, add_producer, edit_producer, remove_producer, remove_producer_confirmation
)
from transactions.views.suppliers_view import (
    suppliers_list, add_supplier, edit_supplier, remove_supplier, remove_supplier_confirmation
)
from transactions.views.clients_view import (
    clients_list, add_client, edit_client, remove_client, remove_client_confirmation
)
from transactions.views.transactions_view import (
    transactions_list, add_transaction, edit_transaction, remove_transaction, remove_transaction_confirmation
)
# from transactions.views.stocks_view import (
#     stocks_list
# )
from transactions.views.provinces_view import load_provinces

from transactions.views.clients_view import ClientListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('transactions.urls')),
    path('api/', include('transactions.api.urls', namespace='api')),
    
    #Path Authentication
    path('accounts/', include('allauth.urls')),
    
    #Path personnalisés Front
    path('', producers_list, name='home'),
    path('load-provinces/', load_provinces, name='load_provinces'),
     
    #producers
    path('producers/', producers_list, name='producers_list'),
    path('producers/add', add_producer, name='add_producer'),
    path('producers/<int:pk>/edit', edit_producer, name='edit_producer'),
    path('producers/<int:pk>/remove_confirmation', remove_producer_confirmation, name='remove_producer_confirmation'),
    path('producers/<int:pk>/remove', remove_producer, name='remove_producer'),
    
    #suppliers
    path('suppliers/', suppliers_list, name='suppliers_list'),
    # path('suppliers/<int:pk>/', supplier_detail, name='supplier_detail'),
    path('suppliers/add', add_supplier, name='add_supplier'),
    path('suppliers/<int:pk>/edit', edit_supplier, name='edit_supplier'),
    path('suppliers/<int:pk>/remove_confirmation', remove_supplier_confirmation, name='remove_supplier_confirmation'),
    path('suppliers/<int:pk>/remove', remove_supplier, name='remove_supplier'),
    
    #clients
    path('clients/', TemplateView.as_view(template_name='transactions/clients/clients_list.html'), name='clients_list'),
    # path('clients_list/', ClientListAPIView.as_view(), name='clients_list'),
    
    # path('clients/', clients_list, name='clients_list'),
    # path('clients/add', add_client, name='add_client'),
    # path('clients/<int:pk>/edit', edit_client, name='edit_client'),
    # path('clients/<int:pk>/remove_confirmation', remove_client_confirmation, name='remove_client_confirmation'),
    # path('clients/<int:pk>/remove', remove_client, name='remove_client'),
    
    #transactions
    path('transactions/', transactions_list, name='transactions_list'),
    path('transactions/add', add_transaction, name='add_transaction'),
    path('transactions/<int:pk>/edit', edit_transaction, name='edit_transaction'),
    path('transactions/<int:pk>/remove_confirmation', remove_transaction_confirmation, name='remove_transaction_confirmation'),
    path('transactions/<int:pk>/remove', remove_transaction, name='remove_transaction'),
    
    #stocks
    # path('stocks/', stocks_list, name='stocks_list'),
    # path('stocks/add', add_stock, name='add_stock'),
    # path('stocks/<int:pk>/edit', edit_stock, name='edit_stock'),
    # path('stocks/<int:pk>/remove_confirmation', remove_stock_confirmation, name='remove_stock_confirmation'),
    # path('stocks/<int:pk>/remove', remove_stock, name='remove_stock'),
    
    
]

