# views.py

from django.http import JsonResponse
from ..models import Product, Supplier, Client, Producer, UniqueSector
from django.views.decorators.http import require_GET
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# def get_products(request):
#     if request.method == 'GET' and request.is_ajax():
#         sector_labels = request.GET.getlist('sector_labels[]')
#         products = Product.objects.filter(sector_label__name__in=sector_labels).distinct()
#         products_data = [{'id': product.id, 'name': product.name} for product in products]
#         return JsonResponse({'products': products_data})
#     return JsonResponse({}, status=400)

@login_required
def get_user(request):
    producer = getattr(request.user, 'producer', None)
    context = {
        'user': request.user,
        'producer': producer,
    }
    return render(request, 'transactions/components/header.html', context)

@require_GET
def get_products(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Récupérer les identifiants de sector_labels de la requête GET
        sector_ids = request.GET.getlist('sector_labels[]')
        # print(f"Received sector_ids: {sector_ids}")  # Log the received sector_ids
        
        if not sector_ids:
            # print("No sector_is provided")  # Log the lack of sector_ids    
            return JsonResponse({'products': [], 'message': 'Aucun éléments'}, status=200)
        
        try:
            # Récupérer les sector_labels correspondants aux sector_ids
            sector_labels = UniqueSector.objects.filter(id__in=sector_ids).values_list('sector_label', flat=True)
            # print(f"Corresponding sector_labels: {list(sector_labels)}")  # Log the corresponding sector_labels
            
            # Filtrer les produits par sector_label
            products = Product.objects.filter(sector_label__in=sector_labels).distinct()
            products_data = [{'id': product.id, 'product_label': product.product_label, 'sector_label': product.sector_label} for product in products]
            # print(f"Filtered products: {products_data}")  # Log the filtered products
            return JsonResponse({'products': products_data})
        except Exception as e:
            # print(f"Error while fetching products: {e}")  # Log any errors
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def filter_products_by_producer(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        producer_id = request.GET.get('producer_id')
        products = Product.objects.filter(producer__id=producer_id).values('id', 'product_label')
        products_list = list(products)
        return JsonResponse({'products': products_list})
    else:
        return JsonResponse({'error': 'Invalid request'})

def filter_producer_details(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        producer_id = request.GET.get('producer_id')
        
        # Récupérer le producteur
        try:
            producer = Producer.objects.get(id=producer_id)
        except Producer.DoesNotExist:
            return JsonResponse({'error': 'Producer does not exist'})

        # Récupérer les produits
        products = producer.product.values('id', 'product_label')
        products_list = list(products)

        # Récupérer les fournisseurs
        suppliers = producer.suppliers.values('id', 'category', 'name')
        suppliers_list = [
            {
                'id': supplier['id'],
                'name': supplier['name']
            }
            for supplier in suppliers
        ]

        # Récupérer les clients
        clients = producer.clients.values('id', 'category', 'name')
        clients_list = [
            {
                'id': client['id'],
                'name': client['name']
            }
            for client in clients
        ]

        return JsonResponse({
            'products': products_list,
            'suppliers': suppliers_list,
            'clients': clients_list
        })
    else:
        return JsonResponse({'error': 'Invalid request'})

# def products_by_sector(request):
#     if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         sector_label = request.GET.get('sector_label')
        
#         if not sector_label:
#             return JsonResponse({'error': 'No sector_label provided'}, status=400)
        
#         # Supposons que sector_label est une liste de valeurs dans le cas de SelectMultiple
#         if isinstance(sector_label, str):
#             sector_labels = sector_label.split(',')
#         else:
#             sector_labels = sector_label
        
#         # Filtrer les produits par les labels de secteur
#         products = Product.objects.filter(sector_label__in=sector_labels).values('id', 'product_label')
#         products_list = list(products)
        
#         return JsonResponse({'products': products_list})
    
#     return JsonResponse({'error': 'Invalid request'}, status=400)

# def filter_producer_details(request):
#     if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         producer_id = request.GET.get('producer_id')
#         products = Product.objects.filter(producer__id=producer_id).values('id', 'product_label')
#         suppliers = Supplier.objects.filter(producer__id=producer_id).values('id', 'name', 'company_name')
#         clients = Client.objects.filter(producer__id=producer_id).values('id', 'name', 'company_name')
        
#         products_list = list(products)
#         suppliers_list = list(suppliers)
#         clients_list = list(clients)
#         return JsonResponse({'products': products_list, 'suppliers': suppliers_list, 'clients': clients_list})
#     else:
#         return JsonResponse({'error': 'Invalid request'})
        