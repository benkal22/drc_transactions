from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.http import urlencode
from django_htmx.http import retarget
from django.db.models import F, ExpressionWrapper, DecimalField, Sum

from transactions.models import Client, Producer, Product, UniqueSector, Country, Province
from transactions.forms import ClientForm
from transactions.filters import ClientFilter

@login_required
def client_statistics(request):
    # Appliquer le filtre des clients
    if request.user.is_superuser:
        queryset = Client.objects.all()
    else:
        producer = get_object_or_404(Producer, user=request.user)
        queryset = Client.objects.filter(producer=producer)
        
    client_filter =ClientFilter(request.GET, queryset=queryset)
    
    # client_filter = ClientFilter(request.GET, queryset=Client.objects.all())
    filtered_clients = client_filter.qs

    # Montant général de toutes les ventes
    total_sales = filtered_clients.aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0.00

    # Nombre total de tous les clients
    total_clients = filtered_clients.count()

    # Nombre total des clients de catégorie entreprise
    total_enterprise_clients = filtered_clients.filter(category='enterprise').count()

    # Nombre total des clients de catégorie individuel
    total_individual_clients = filtered_clients.filter(category='individual').count()

    # Montant de toutes les ventes des clients entreprise
    total_sales_enterprises = filtered_clients.filter(category='enterprise').aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0.00

    # Montant de toutes les ventes des clients individuels
    total_sales_individuals = filtered_clients.filter(category='individual').aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0.00

    # Calculer les revenus nets
    net_income_enterprises = total_sales - total_sales_enterprises
    net_income_individuals = total_sales - total_sales_individuals

    # Éviter les valeurs négatives pour les revenus nets
    net_income_enterprises_display = f"➕{net_income_enterprises:.2f}" if net_income_enterprises > 0 else f"➖{abs(net_income_enterprises):.2f}"
    net_income_individuals_display = f"➕{net_income_individuals:.2f}" if net_income_individuals > 0 else f"➖{abs(net_income_individuals):.2f}"

    # Retourner les résultats sous forme de dictionnaire
    return {
        'total_sales': f"💰{total_sales:.2f} {filtered_clients.first()}",
        'total_clients': total_clients,
        'total_enterprise_clients': total_enterprise_clients,
        'total_individual_clients': total_individual_clients,
        'total_sales_enterprises': f"💰{total_sales_enterprises:.2f} {filtered_clients.first()}",
        'total_sales_individuals': f"💰{total_sales_individuals:.2f} {filtered_clients.first()}",
        'net_income_enterprises': net_income_enterprises_display,
        'net_income_individuals': net_income_individuals_display
    }

@login_required
def clients_list(request):
    if request.user.is_superuser:
        queryset = Client.objects.all()
    else:
        producer = get_object_or_404(Producer, user=request.user)
        queryset = Client.objects.filter(producer=producer)
        
    client_filter =ClientFilter(request.GET, queryset=queryset)
    
    filtered_clients = client_filter.qs

    paginator = Paginator(filtered_clients, 10)
    page = request.GET.get('page')

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)
    
    filter_params = urlencode(request.GET)
    
    # Obtenez les statistiques en appelant la fonction client_statistics
    stats = client_statistics(request)

    context = {
        'filter': client_filter,
        'filter_params': filter_params,
        'clients': clients,
        'total_sales': stats['total_sales'],
        'total_clients': stats['total_clients'],
        'total_enterprise_clients': stats['total_enterprise_clients'],
        'total_individual_clients': stats['total_individual_clients'],
        'total_sales_enterprises': stats['total_sales_enterprises'],
        'total_sales_individuals': stats['total_sales_individuals'],
        'net_income_enterprises': stats['net_income_enterprises'],
        'net_income_individuals': stats['net_income_individuals']
    }
    
    if request.htmx:
        return render(request, 'transactions/clients/partials/clients-container.html', context)

    return render(request, 'transactions/clients/clients-list.html', context)

def client_detail(request, pk):
    # Récupérer le client avec l'ID donné
    if request.user.is_superuser:
        client = get_object_or_404(Client, pk=pk)
    else:
        producer = get_object_or_404(Producer, user=request.user)
        client = get_object_or_404(Client, pk=pk, producer=producer)
    
    stats = client_statistics(request)

    context = {
        'client': client,  
        'total_sales': stats['total_sales'],
        'total_clients': stats['total_clients'],
        'total_enterprise_clients': stats['total_enterprise_clients'],
        'total_individual_clients': stats['total_individual_clients'],
        'total_sales_enterprises': stats['total_sales_enterprises'],
        'total_sales_individuals': stats['total_sales_individuals'],
        'net_income_enterprises': stats['net_income_enterprises'],
        'net_income_individuals': stats['net_income_individuals']
    }
    return render(request, 'transactions/clients/partials/client-detail.html', context)

@login_required
def create_client_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save(commit=False)
            # Associer le producteur connecté au client
            producer = get_object_or_404(Producer, user=request.user)
            client.save()  # Sauvegarder l'instance du client en premier
            client.producer.set([producer])  # Utiliser la méthode set() pour assigner le producteur
            messages.success(request, f"Client '{client}' créé avec succès.")
            context = {'message': f"Client '{client.id}' '{client.name}' enregistré avec succès !"}
            return render(request, 'transactions/clients/partials/client-success.html', context)
        else:
            messages.error(request, "Erreur lors de la création du client. Veuillez vérifier les informations fournies.")
            context = {'form': form}
            response = render(request, 'transactions/clients/partials/client-create.html', context)
            return retarget(response, '#client-block')
        
    context = {'form': ClientForm()}
    return render(request, 'transactions/clients/partials/client-create.html', context)

@login_required
def update_client(request, pk):
    if request.user.is_superuser:
        client = get_object_or_404(Client, pk=pk)
    else:
        producer = get_object_or_404(Producer, user=request.user)
        client = get_object_or_404(Client, pk=pk, producer=producer)
        
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            context = {'message': f"Client '{client.id}' '{client.name}' mis à jour avec succès !"}
            return render(request, 'transactions/clients/partials/client-success.html', context)
        else:
            context = {
                'form': form,
                'client': client,
            }
            response = render(request, 'transactions/clients/partials/client-update.html', context)
            return retarget(response, '#client-block')
        
    context = {
        'form': ClientForm(instance=client),
        'client': client,
    }
    return render(request, 'transactions/clients/partials/client-update.html', context)

@login_required
@require_http_methods(["DELETE"])
def delete_client(request, pk):
    if request.user.is_superuser:
        client = get_object_or_404(Client, pk=pk)
    else:
        producer = get_object_or_404(Producer, user=request.user)
        client = get_object_or_404(Client, pk=pk, producer=producer)

    client.delete()
    messages.success(request, f"Client '{client}' supprimé avec succès.")
    return redirect('transactions:clients_list')
