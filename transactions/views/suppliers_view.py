from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.http import urlencode
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_htmx.http import retarget
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
import json

from transactions.models import Supplier, ProducerSupplier, Transaction, Product, UniqueSector, Country, Province
from transactions.serializers import SupplierSerializer
from transactions.filters import SupplierFilter
from transactions.forms import SupplierForm

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

@login_required
def supplier_statistics(request):
    # Appliquer le filtre des fournisseurs
    supplier_filter = SupplierFilter(request.GET, queryset=Supplier.objects.all())
    filtered_suppliers = supplier_filter.qs

    # Montant général de tous les achats effectués par le producer aux suppliers en CDF
    total_purchases = filtered_suppliers.aggregate(total_purchases=Sum('total_purchases'))['total_purchases'] or 0.00

    # Nombre total de tous les fournisseurs
    total_suppliers = filtered_suppliers.count()

    # Nombre total des fournisseurs de catégorie entreprise
    total_enterprise_suppliers = filtered_suppliers.filter(category='enterprise').count()

    # Nombre total des fournisseurs de catégorie individuel
    total_individual_suppliers = filtered_suppliers.filter(category='individual').count()

    # Montant de tous les achats des fournisseurs entreprise
    total_purchases_enterprises = filtered_suppliers.filter(category='enterprise').aggregate(total_purchases=Sum('total_purchases'))['total_purchases'] or 0.00

    # Montant de tous les achats des fournisseurs individuels
    total_purchases_individuals = filtered_suppliers.filter(category='individual').aggregate(total_purchases=Sum('total_purchases'))['total_purchases'] or 0.00

    # Calculer les revenus nets
    net_income_enterprises = total_purchases - total_purchases_enterprises
    net_income_individuals = total_purchases - total_purchases_individuals

    # Éviter les valeurs négatives pour les revenus nets
    net_income_enterprises_display = f"➕{net_income_enterprises:.2f}" if net_income_enterprises > 0 else f"➖{abs(net_income_enterprises):.2f}"
    net_income_individuals_display = f"➕{net_income_individuals:.2f}" if net_income_individuals > 0 else f"➖{abs(net_income_individuals):.2f}"

    # Retourner les résultats sous forme de dictionnaire
    return {
        'total_purchases': f"💰{total_purchases:.2f} CDF",
        'total_suppliers': total_suppliers,
        'total_enterprise_suppliers': total_enterprise_suppliers,
        'total_individual_suppliers': total_individual_suppliers,
        'total_purchases_enterprises': f"💰{total_purchases_enterprises:.2f} CDF",
        'total_purchases_individuals': f"💰{total_purchases_individuals:.2f} CDF",
        'net_income_enterprises': net_income_enterprises_display,
        'net_income_individuals': net_income_individuals_display
    }

@login_required
def suppliers_list(request):
    supplier_filter = SupplierFilter(
        request.GET,
        queryset=Supplier.objects.all()
    )
    
    filtered_suppliers = supplier_filter.qs

    paginator = Paginator(filtered_suppliers, 10)
    page = request.GET.get('page')

    try:
        suppliers = paginator.page(page)
    except PageNotAnInteger:
        suppliers = paginator.page(1)
    except EmptyPage:
        suppliers = paginator.page(paginator.num_pages)
    
    filter_params = urlencode(request.GET)
    
    # Obtenez les statistiques en appelant la fonction supplier_statistics
    stats = supplier_statistics(request)

    context = {
        'filter': supplier_filter,
        'filter_params': filter_params,
        'suppliers': suppliers,
        'total_purchases': stats['total_purchases'],
        'total_suppliers': stats['total_suppliers'],
        'total_enterprise_suppliers': stats['total_enterprise_suppliers'],
        'total_individual_suppliers':  stats['total_individual_suppliers'],
        'total_purchases_enterprises': stats['total_purchases_enterprises'],
        'total_purchases_individuals':stats['total_purchases_individuals'],
        'net_income_enterprises': stats['net_income_enterprises'],
        'net_income_individuals': stats['net_income_individuals'],    
    }
    
    if request.htmx:
        return render(request, 'transactions/suppliers/partials/suppliers-container.html', context)

    return render(request, 'transactions/suppliers/suppliers-list.html', context)

def supplier_detail(request, pk):
    # Récupérer le fournisseur avec l'ID donné
    supplier = get_object_or_404(Supplier, pk=pk)
    
    stats = supplier_statistics(request)

    context = {
        'supplier': supplier,  
        'total_purchases': stats['total_purchases'],
        'total_suppliers': stats['total_suppliers'],
        'total_enterprise_suppliers': stats['total_enterprise_suppliers'],
        'total_individual_suppliers':  stats['total_individual_suppliers'],
        'total_purchases_enterprises': stats['total_purchases_enterprises'],
        'total_purchases_individuals':stats['total_purchases_individuals'],
        'net_income_enterprises': stats['net_income_enterprises'],
        'net_income_individuals': stats['net_income_individuals'],
    }
    return render(request, 'transactions/suppliers/partials/supplier-detail.html', context)

@login_required
def create_supplier_view(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            supplier = form.save()
            messages.success(request, f"Fournisseur '{supplier}' créé avec succès.")
            context = {'message': f"Fournisseur '{supplier.id}' '{supplier.name}' enregistrée avec succès !"}
            return render(request, 'transactions/suppliers/partials/supplier-success.html', context)
        else:
            messages.error(request, "Erreur lors de la création du fournisseur. Veuillez vérifier les informations fournies.")
            context = {'form': form}
            response = render(request, 'transactions/suppliers/partials/supplier-create.html', context)
            return retarget(response, '#supplier-block')
        
    context = {'form': SupplierForm()}
    return render(request, 'transactions/suppliers/partials/supplier-create.html', context)

@login_required
def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            context = {'message': f"Fournisseur '{supplier.id}' '{supplier.name}' mise à jour avec succès !"}
            return render(request, 'transactions/suppliers/partials/supplier-success.html', context)
        else:
            context = {
                'form': form,
                'supplier': supplier,
            }
            response = render(request, 'transactions/suppliers/partials/supplier-update.html', context)
            return retarget(response, '#supplier-block')
        
    context = {
        'form': SupplierForm(instance=supplier),
        'supplier': supplier,
    }
    return render(request, 'transactions/suppliers/partials/supplier-update.html', context)


@login_required
@require_http_methods(["DELETE"])
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    # messages.success(request, f"Fournisseur '{supplier}' supprimé avec succès.")
    return redirect('suppliers_list')



