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

from transactions.views.producers_view import (
    producers_list, add_producer, edit_producer, remove_producer, remove_producer_confirmation
)
# from transactions.views.suppliers_view import (
#     suppliers_list, add_supplier, edit_supplier, remove_supplier, remove_supplier_confirmation
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('transactions.urls')),
    
    #Path Authentication
    path('accounts/', include('allauth.urls')),
    
    #Path personnalisés Front
    path('', producers_list, name='home'),
    
    #producers
    path('producers', producers_list, name='producers_list'),
    path('producers/add', add_producer, name='add_producer'),
    path('producers/<int:pk>/edit', edit_producer, name='edit_producer'),
    path('producers/<int:pk>/remove_confirmation', remove_producer_confirmation, name='remove_producer_confirmation'),
    path('producers/<int:pk>/remove', remove_producer, name='remove_producer'),
    
    #suppliers
    # path('suppliers', suppliers_list, name='suppliers_list'),
    # path('suppliers/add', add_supplier, name='add_supplier'),
    # path('suppliers/<int:pk>/edit', edit_supplier, name='edit_supplier'),
    # path('suppliers/<int:pk>/remove_confirmation', remove_supplier_confirmation, name='remove_supplier_confirmation'),
    # path('suppliers/<int:pk>/remove', remove_supplier, name='remove_supplier'),
    
]

