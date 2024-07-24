#transactions/views/stocks_view.py

from django.shortcuts import render
from rest_framework import viewsets
from ..serializers import StockSerializer
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.http import require_POST
from transactions.forms import StockForm
from django.shortcuts import redirect

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from transactions.models import Stock, Transaction, Producer, Product

from transactions.filters import StockFilter
from transactions.forms import StockForm
from django_htmx.http import retarget
from django.db import models  

from django.db.models import F, ExpressionWrapper, DecimalField, Sum

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.http import urlencode

from django.http import JsonResponse, HttpResponse


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

@login_required
def stocks_list(request):
    if request.user.is_superuser:
        queryset = Stock.objects.all()
    else:
        producer = get_object_or_404(Producer, user=request.user)
        queryset = Stock.objects.filter(producer=producer)
        
    stock_filter = StockFilter(request.GET, queryset=queryset)
    
    filtered_stocks = stock_filter.qs
    
    paginator = Paginator(filtered_stocks, 10)
    page = request.GET.get('page')

    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        stocks = paginator.page(1)
    except EmptyPage:
        stocks = paginator.page(paginator.num_pages)
    
    filter_params = urlencode(request.GET)
    
    # Sérialisation des détails des stocks pour les stocks paginés
    stock_details = {stock.pk: stock.get_details() for stock in stocks}
    stock_details_json = json.dumps(stock_details, cls=DjangoJSONEncoder)

    context = {
        'filter': stock_filter,
        'filter_params': filter_params,
        'stocks': stocks,
        'stock_details_json': mark_safe(stock_details_json),
    }

    if request.htmx:
        return render(request, 'transactions/stocks/partials/stocks-container.html', context)

    return render(request, 'transactions/stocks/stocks-list.html', context)

@login_required
def stock_detail(request, pk):
    if request.user.is_superuser:
        stock = get_object_or_404(Stock, pk=pk)
    else:
        producer = get_object_or_404(Producer, user=request.user)
        stock = get_object_or_404(Stock, pk=pk, producer=producer)
        
    stock_details = stock.get_details()

    context = {
        'stock': stock,
        'stock_details': stock_details,
    }

    if request.htmx:
        return render(request, 'transactions/stocks/partials/stock-detail.html', context)

    return render(request, 'transactions/stocks/partials/stock-detail.html', context)

@login_required
def create_stock_view(request):
    producer = get_object_or_404(Producer, user=request.user)
    if request.method == 'POST':
        form = StockForm(request.POST, producer=producer)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.producer = producer
            stock.save()
            context = {'message': f"Stock for product '{stock.product}' created successfully."}
            return render(request, 'transactions/stocks/partials/stock-success.html', context)
        else:
            context = {'form': form}
            response = render(request, 'transactions/stocks/partials/stock-create.html', context)
            return retarget(response, '#stock-block')

    context = {'form': StockForm(producer=producer)}
    return render(request, 'transactions/stocks/partials/stock-create.html', context)

# @login_required
# def create_stock_view(request):
#     if request.method == 'POST':
#         form = StockForm(request.POST, request.FILES)
#         if form.is_valid():
#             stock = form.save(commit=False)
#             # Associer le producteur connecté au stock
#             producer = get_object_or_404(Producer, user=request.user)
#             stock.save()  # Sauvegarder le stock pour obtenir l'ID
#             stock.producer.set([producer])  # Utiliser .set() pour les ManyToManyFields
#             stock.save() 
#             messages.success(request, f"Stock '{stock}' déclaré avec succès.")
#             context = {'message': f"Stock '{stock.id}' '{stock.name}' enregistré avec succès !"}
#             return render(request, 'transactions/stocks/partials/stock-success.html', context)
#         else:
#             messages.error(request, "Erreur lors de la création du stock. Veuillez vérifier les informations fournies.")
#             context = {'form': form}
#             response = render(request, 'transactions/stocks/partials/stock-create.html', context)
#             return retarget(response, '#stock-block')
        
#     context = {'form': StockForm()}
#     return render(request, 'transactions/stocks/partials/stock-create.html', context)


@login_required
def stock_update(request, pk):
    if request.user.is_superuser:
        stock = get_object_or_404(Stock, pk=pk)
    else:
        producer = get_object_or_404(Producer, user=request.user)
        stock = get_object_or_404(Stock, pk=pk, producer=producer)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            stock = form.save()
            context = {'message': f"Stock for product '{stock.product}' updated successfully."}
            return render(request, 'transactions/stocks/partials/stock-success.html', context)
        else:
            context = {
                'form': form,
                'stock': stock,
            }
            response = render(request, 'transactions/stocks/partials/stock-update.html', context)
            return retarget(response, '#stock-block')
        
    context = {
        'form': StockForm(instance=stock),
        'stock': stock,
    }
    return render(request, 'transactions/stocks/partials/stock-update.html', context)

@login_required
@require_http_methods(["DELETE"])
def delete_stock(request, pk):
    if request.user.is_superuser:
        stock = get_object_or_404(Stock, pk=pk)
    else:
        producer = get_object_or_404(Producer, user=request.user)
        stock = get_object_or_404(Stock, pk=pk, producer=producer)
        
    stock.delete()
    context = {
        'message': f"Stock for product '{stock.product}' was deleted successfully!"
    }
    return render(request, 'transactions/stocks/partials/stock-success.html', context)
