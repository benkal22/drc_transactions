from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from transactions.views.base_views import (filter_products_by_producer,  filter_producer_details,  
                                           get_products
                                           ) 
from transactions.views.transactions_view import (transactions_list, create_transaction_view,
                                                  update_transaction, delete_transaction, transaction_detail,
                                                  )
from transactions.views.clients_view import (clients_list, create_client_view,
                                                  update_client, delete_client, client_detail,
                                                  )
from transactions.views.suppliers_view import (suppliers_list, create_supplier_view,
                                                  update_supplier, delete_supplier, supplier_detail,
                                                  )
from transactions.views.producers_view import (producers_list, create_producer_view,
                                                  update_producer, delete_producer, producer_detail,
                                                  )
from transactions.views.dashboard_view import DashboardListView, reports_provinces
from transactions.views.dashboard_view import dashboard_view
from transactions.views.producers2_view import ProducerListViewSet

from django.conf import settings
from django.conf.urls.static import static

app_name = 'transactions'

urlpatterns = [
    path('profile/', ProducerListViewSet.as_view(), name='profile'), 
    path('transaction_dashboard/', dashboard_view, name='transaction_dashboard'),
    path('filter-producer-details/', filter_producer_details, name='filter_producer_details'),
    path('filter-products-by-producer/', filter_products_by_producer, name='filter_products'),
    path('products-by-sector/', get_products, name='products_by_sector'), 
 
    path('transactions/', transactions_list, name='transactions_list'), 
    path('transactions/<int:pk>/update/', update_transaction, name='transaction_update'),
    path('transactions/<int:pk>/delete/', delete_transaction, name='transaction_delete'),
    path('transaction/<int:pk>/', transaction_detail, name='transaction_detail'),
    path('transactions/create/', create_transaction_view, name='transaction_create'),
    
    path('suppliers/', suppliers_list, name='suppliers_list'), 
    path('suppliers/<int:pk>/update/', update_supplier, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', delete_supplier, name='supplier_delete'),
    path('supplier/<int:pk>/', supplier_detail, name='supplier_detail'),
    path('suppliers/create/', create_supplier_view, name='supplier_create'),
    
    path('producers/', producers_list, name='producers_list'), 
    path('producers/<int:pk>/update/', update_producer, name='producer_update'),
    path('producers/<int:pk>/delete/', delete_producer, name='producer_delete'),
    path('producer/<int:pk>/', producer_detail, name='producer_detail'),
    path('producers/create/', create_producer_view, name='producer_create'),
    
    path('clients/', clients_list, name='clients_list'), 
    path('clients/<int:pk>/update/', update_client, name='client_update'),
    path('clients/<int:pk>/delete/', delete_client, name='client_delete'),
    path('client/<int:pk>/', client_detail, name='client_detail'),
    path('clients/create/', create_client_view, name='client_create'),
    
    path('home_page/', login_required(TemplateView.as_view(template_name='transactions/home_page.html')), name='home_page'),  # Page d'accueil sécurisée
    path('reports/', login_required(TemplateView.as_view(template_name='transactions/reports/reports.html')), name='reports'),  # Rapports sécurisés
    path('contact/', login_required(TemplateView.as_view(template_name='transactions/pages/contact.html')), name='contact'),  # Page de contact sécurisée
    path('about/', login_required(TemplateView.as_view(template_name='transactions/reports/pages/about.html')), name='about'),  # Page "À propos" sécurisée
    path('blank/', login_required(TemplateView.as_view(template_name='transactions/pages/blank.html')), name='blank'),  # Page vide sécurisée
    path('404/', login_required(TemplateView.as_view(template_name='transactions/pages/404.html')), name='page_404'),  # Page 404 sécurisée
    path('404/', login_required(TemplateView.as_view(template_name='transactions/pages/settings.html')), name='settings'),  # Page 404 sécurisée
    
    path('dashboard/', DashboardListView.as_view(), name='dashboard'),  # Tableau de bord sécurisé
    path('reports_provinces/', reports_provinces, name='reports_provinces'),  # Tableau de bord sécurisé
    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)