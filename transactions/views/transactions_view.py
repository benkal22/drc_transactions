#transactions/views/transactions_view.py

from django.shortcuts import render
from rest_framework import viewsets
from ..models import Transaction
from ..serializers import TransactionSerializer
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.http import require_POST
from transactions.forms import TransactionForm
from django.shortcuts import redirect

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from transactions.models import Transaction, Producer, Product

from transactions.filters import TransactionFilter
from transactions.forms import TransactionForm
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

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

@login_required
def transaction_statistics(request):
    if request.user.is_superuser:
        queryset = Transaction.objects.all()
    else:
        queryset = Transaction.objects.filter(user=request.user)
        
    transaction_filter = TransactionFilter(request.GET, queryset=queryset)
    
    filtered_transactions = transaction_filter.qs

    total_purchases = filtered_transactions.filter(type='purchase').aggregate(
        total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField()))
    )['total'] or 0

    total_sales = filtered_transactions.filter(type='sale').aggregate(
        total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField()))
    )['total'] or 0
    
    total_clients = filtered_transactions.filter(client__isnull=False).values('client').distinct().count()
    
    net_income =  total_purchases - total_sales
    
    total_quantities_sales = float(filtered_transactions.filter(type='sale').aggregate(
        total=Sum('quantity')
    )['total'] or 0)
    
    total_quantities_purchases = float(filtered_transactions.filter(type='purchase').aggregate(
        total=Sum('quantity')
    )['total'] or 0)

    stock = total_quantities_purchases - total_quantities_sales
    
    # Format stock with emoji signs
    stock_display = f"➕{int(stock)}" if stock > 0 else f"➖{int(abs(stock))}"

    # Format net income with emoji signs
    # net_income_display = f"➕{net_income:.2f}" if net_income > 0 else f"➖{abs(net_income):.2f}"

    return {
        'total_purchases': total_purchases,
        'total_sales': total_sales,
        'total_clients': total_clients,
        'net_income': net_income,
        'stock': stock_display
    }

@login_required
def transactions_list(request):
    if request.user.is_superuser:
        queryset = Transaction.objects.all()
    else:
        queryset = Transaction.objects.filter(user=request.user)
        
    transaction_filter = TransactionFilter(request.GET, queryset=queryset)
    
    filtered_transactions = transaction_filter.qs

    # Obtenez les statistiques en appelant la fonction transaction_statistics
    stats = transaction_statistics(request)
    
    paginator = Paginator(filtered_transactions, 10)
    page = request.GET.get('page')

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    
    filter_params = urlencode(request.GET)
    
    # Sérialisation des détails des transactions pour les transactions paginées
    transaction_details = {transaction.pk: transaction.get_details() for transaction in transactions}
    transaction_details_json = json.dumps(transaction_details, cls=DjangoJSONEncoder)

    context = {
        'filter': transaction_filter,
        'filter_params': filter_params,
        'transactions': transactions,
        'total_sales': stats['total_sales'],
        'total_purchases': stats['total_purchases'],
        'total_clients': stats['total_clients'],
        'net_income': stats['net_income'],
        'stock': stats['stock'],
        'transaction_details_json': mark_safe(transaction_details_json),
    }

    if request.htmx:
        return render(request, 'transactions/transactions/partials/transactions-container.html', context)

    return render(request, 'transactions/transactions/transactions-list.html', context)

@login_required
def transaction_detail(request, pk):
    if request.user.is_superuser:
        transaction = get_object_or_404(Transaction, pk=pk)
    else:
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        
    transaction_details = transaction.get_details()

    context = {
        'transaction': transaction,
        'transaction_details': transaction_details,
    }

    if request.htmx:
        return render(request, 'transactions/transactions/partials/transaction-detail.html', context)

    return render(request, 'transactions/transactions/partials/transaction-detail.html', context)

@login_required
def create_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'message': f"Transaction n°'{transaction.id}' en date de '{transaction.date}' enregistrée avec succès."}
            return render(request, 'transactions/transactions/partials/transaction-success.html', context)
        else:
            context = {'form': form}
            response = render(request, 'transactions/transactions/partials/transaction-create.html', context)
            return retarget(response, '#transaction-block')

    context = {'form': TransactionForm()}
    return render(request, 'transactions/transactions/partials/transaction-create.html', context)

@login_required
def update_transaction(request, pk):
    if request.user.is_superuser:
        transaction = get_object_or_404(Transaction, pk=pk)
    else:
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            context = {'message': f"Transaction n°'{transaction.id}' en date de '{transaction.date}' mise à jour avec succès !"}
            return render(request, 'transactions/transactions/partials/transaction-success.html', context)
        else:
            context = {
                'form': form,
                'transaction': transaction,
            }
            response = render(request, 'transactions/transactions/partials/transaction-update.html', context)
            return retarget(response, '#transaction-block')
        
    context = {
        'form': TransactionForm(instance=transaction),
        'transaction': transaction,
    }
    return render(request, 'transactions/transactions/partials/transaction-update.html', context)

@login_required
@require_http_methods(["DELETE"])
def delete_transaction(request, pk):
    if request.user.is_superuser:
        transaction = get_object_or_404(Transaction, pk=pk)
    else:
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    context = {
        'message': f"Transaction of {transaction.total_price_cdf()} on {transaction.date} was deleted successfully!"
    }
    return render(request, 'transactions/transactions/partials/transaction-success.html', context)
    