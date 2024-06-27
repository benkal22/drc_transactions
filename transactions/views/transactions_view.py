#transactions/views/transactions_view.py

from django.shortcuts import render
from rest_framework import viewsets
from ..models import Transaction
from ..serializers import TransactionSerializer

from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.http import require_POST
from transactions.forms import TransactionForm
from django.shortcuts import redirect

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
        
def transactions_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions/transactions/transactions_list.html', {'transactions': transactions})

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save()
            return redirect('transactions_list')  # Redirige vers transactions_list
        else:
            return render(request, 'transactions/transactions/transaction_form.html', {'form': form})
    else:
        form = TransactionForm()
    return render(request, 'transactions/transactions/transaction_form.html', {'form': form})

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            return redirect('transactions_list')  # Redirige vers transactions_list
        else:
            return render(request, 'transactions/transactions/transaction_form.html', {'form': form, 'transaction': transaction})
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/transactions/transaction_form.html', {'form': form, 'transaction': transaction})

def remove_transaction_confirmation(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transactions/transactions/transaction_delete_confirmation.html', {'transaction': transaction})

@require_POST
def remove_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    company_name = transaction.date  # Pour l'utilisation dans le message de confirmation
    
    transaction.delete()
    
    # Redirection vers transactions_list avec un message
    return redirect('transactions_list')