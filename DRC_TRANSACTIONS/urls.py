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

from django.contrib import admin
from django.urls import path, include

from .views import CurrencyConversionView, home_redirect, redirect_view
from transactions.views.dashboard_view import CorrelationMatrixView, EconomicsPredictionView, drc_map

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('redirect/', redirect_view, name='redirect_view'),
        
    #Path Authentication
    path('accounts/', include('allauth.urls')),
    
    #API interne
    path('api/', include('transactions.api.urls', namespace='api')),
    
    #url api externe conversion monnaie
    path('convert/', CurrencyConversionView.as_view(), name='currency-convert'),
    
    path('', home_redirect, name='home'),
    path('', include('transactions.urls', namespace='transactions')),
    
    path('matrix/', CorrelationMatrixView.as_view(), name='correlation_matrix'),  # Tableau de bord sécurisé
    path('prediction/', EconomicsPredictionView.as_view(), name='economic_prediction'),  # Tableau de bord sécurisé
    path('drc_map/', drc_map, name='drc_map'),  # Tableau de bord sécurisé

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)