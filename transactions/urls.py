#DRC_TRANSACTIONS/transactions/urls.py
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


app_name = 'transactions'

urlpatterns = [
    path('dashboard/', login_required(TemplateView.as_view(template_name='transactions/dashboard.html')), name='dashboard'),
    path('home_page/', login_required(TemplateView.as_view(template_name='transactions/home_page.html')), name='home_page'),
    path('profil/', login_required(TemplateView.as_view(template_name='transactions/producers/profil.html')), name='profil'),
    path('suppliers/', login_required(TemplateView.as_view(template_name='transactions/suppliers/suppliers.html')), name='suppliers'),
    path('clients/', login_required(TemplateView.as_view(template_name='transactions/clients/clients.html')), name='clients'),
    path('transactions/', login_required(TemplateView.as_view(template_name='transactions/transactions/transactions.html')), name='transactions'),
]