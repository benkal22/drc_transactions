from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.http import urlencode
from django_htmx.http import retarget
from django.db.models import F, ExpressionWrapper, DecimalField, Sum

from transactions.models import Producer, Product, UniqueSector, Country, Province
from transactions.forms import ProducerForm
from transactions.filters import ProducerFilter


@login_required
def producer_statistics(request):
    if request.user.is_superuser:
        queryset = Producer.objects.all()
    else:
        queryset = Producer.objects.filter(user=request.user)
        
    producer_filter = ProducerFilter(request.GET, queryset=queryset)
    filtered_producers = producer_filter.qs

    # Calculer le total des ventes pour tous les clients associés aux producteurs filtrés
    total_sales = filtered_producers.aggregate(
        total_sales=Sum(
            'clients__total_sales'
        )
    )['total_sales'] or 0.00

    # Calculer le total des achats pour tous les fournisseurs associés aux producteurs filtrés
    total_purchases = filtered_producers.aggregate(
        total_purchases=Sum(
            'suppliers__total_purchases'
        )
    )['total_purchases'] or 0.00

    # Nombre total de tous les producteurs
    total_producers = filtered_producers.count()

    # Nombre total des producteurs approuvés
    total_approved_producers = filtered_producers.filter(is_approved=True).count()

    # Nombre total des producteurs non approuvés
    total_unapproved_producers = filtered_producers.filter(is_approved=False).count()

    # Retourner les résultats sous forme de dictionnaire
    return {
        'total_sales': f"💰{total_sales:.2f} CDF",
        'total_purchases': f"💰{total_purchases:.2f} CDF",
        'total_producers': total_producers,
        'total_approved_producers': total_approved_producers,
        'total_unapproved_producers': total_unapproved_producers
    }
@login_required
def producers_list(request):
    if request.user.is_superuser:
        queryset = Producer.objects.all()
    else:
        queryset = Producer.objects.filter(user=request.user)
        
    producer_filter = ProducerFilter(request.GET, queryset=queryset)
    filtered_producers = producer_filter.qs

    paginator = Paginator(filtered_producers, 10)
    page = request.GET.get('page')

    try:
        producers = paginator.page(page)
    except PageNotAnInteger:
        producers = paginator.page(1)
    except EmptyPage:
        producers = paginator.page(paginator.num_pages)
    
    filter_params = urlencode(request.GET)
    
    # Obtenez les statistiques en appelant la fonction producer_statistics
    stats = producer_statistics(request)
    
    welcome = ''
    if request.user.last_login is None or request.user.last_login == request.user.date_joined:   
        welcome = f"Bienvenue ! Compléter votre profile"

    context = {
        'filter': producer_filter,
        'filter_params': filter_params,
        'producers': producers,
        'total_sales': stats['total_sales'],
        'total_purchases': stats['total_purchases'],
        'total_producers': stats['total_producers'],
        'total_approved_producers': stats['total_approved_producers'],
        'total_unapproved_producers': stats['total_unapproved_producers'],
        'welcome': welcome
    }
    
    if request.htmx:
        return render(request, 'transactions/producers/partials/producers-container.html', context)

    return render(request, 'transactions/producers/producers-list.html', context)

def producer_detail(request, pk):
    if request.user.is_superuser:
        producer = get_object_or_404(Producer, pk=pk)
    else:
        producer = get_object_or_404(Producer, pk=pk, user=request.user)
        
    stats = producer_statistics(request)

    context = {
        'producer': producer,  
        'total_sales': stats['total_sales'],
        'total_purchases': stats['total_purchases'],
        'total_producers': stats['total_producers'],
        'total_approved_producers': stats['total_approved_producers'],
        'total_unapproved_producers': stats['total_unapproved_producers']
    }
    return render(request, 'transactions/producers/partials/producer-detail.html', context)

@login_required
def create_producer_view(request):
    if request.method == 'POST':
        form = ProducerForm(request.POST, request.FILES)
        if form.is_valid():
            producer = form.save(commit=False)
            producer.user = request.user
            producer = form.save()
            messages.success(request, f"Producteur '{producer}' créé avec succès.")
            context = {'message': f"Producteur '{producer.id}' '{producer.company_name}' enregistré avec succès !"}
            return render(request, 'transactions/producers/partials/producer-success.html', context)
        else:
            messages.error(request, "Erreur lors de la création du producteur. Veuillez vérifier les informations fournies.")
            context = {'form': form}
            response = render(request, 'transactions/producers/partials/producer-create.html', context)
            return retarget(response, '#producer-block')
        
    context = {'form': ProducerForm()}
    if request.user.is_superuser:
        return render(request, 'transactions/producers/partials/producer-create.html', context)     

@login_required
def producer_update(request, pk):
    if request.user.is_superuser:
        producer = get_object_or_404(Producer, pk=pk)
    else:
        producer = get_object_or_404(Producer, pk=pk, user=request.user)
        
    if request.method == 'POST':
        form = ProducerForm(request.POST, instance=producer)
        if form.is_valid():
            producer = form.save()
            context = {'message': f"Producteur '{producer.id}' '{producer.company_name}' mis à jour avec succès !"}
            return render(request, 'transactions/producers/partials/producer-success.html', context)
        else:
            context = {
                'form': form,
                'producer': producer,
            }
            response = render(request, 'transactions/producers/partials/producer-update.html', context)
            return retarget(response, '#producer-block')
        
    context = {
        'form': ProducerForm(instance=producer),
        'producer': producer,
    }
    return render(request, 'transactions/producers/partials/producer-update.html', context)

@login_required
@require_http_methods(["DELETE"])
def delete_producer(request, pk):
    if request.user.is_superuser:
        producer = get_object_or_404(Producer, pk=pk)
    else:
        producer = get_object_or_404(Producer, pk=pk, user=request.user)
        
    producer.delete()
    messages.success(request, f"Producteur '{producer}' supprimé avec succès.")
    return redirect('transactions:producers_list')
