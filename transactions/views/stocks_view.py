#transactions/views/stocks_view.py

from django.shortcuts import render, redirect
from rest_framework import viewsets
from ..models import Stock
from ..serializers import StockSerializer

from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.http import require_POST
# from transactions.forms import StockForm

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    
def stocks_list(request):
    stocks = Stock.objects.all()
    return render(request, 'transactions/stocks/stocks_list.html', {'stocks': stocks})

# def add_stock(request):
#     if request.method == 'POST':
#         form = StockForm(request.POST, request.FILES)
#         if form.is_valid():
#             stock = form.save()
#             return redirect('stocks_list')  # Redirige vers stocks_list
#         else:
#             return render(request, 'transactions/stocks/stock_form.html', {'form': form})
#     else:
#         form = StockForm()
#     return render(request, 'transactions/stocks/stock_form.html', {'form': form})

# def edit_stock(request, pk):
#     stock = get_object_or_404(Stock, pk=pk)
#     if request.method == 'POST':
#         form = StockForm(request.POST, request.FILES, instance=stock)
#         if form.is_valid():
#             stock = form.save()
#             return redirect('stocks_list')  # Redirige vers stocks_list
#         else:
#             return render(request, 'transactions/stocks/stock_form.html', {'form': form, 'stock': stock})
#     else:
#         form = StockForm(instance=stock)
#     return render(request, 'transactions/stocks/stock_form.html', {'form': form, 'stock': stock})

# def remove_stock_confirmation(request, pk):
#     stock = get_object_or_404(Stock, pk=pk)
#     return render(request, 'transactions/stocks/stock_delete_confirmation.html', {'stock': stock})

# @require_POST
# def remove_stock(request, pk):
#     stock = get_object_or_404(Stock, pk=pk)
#     company_name = stock.date  # Pour l'utilisation dans le message de confirmation
    
#     stock.delete()
    
#     # Redirection vers stocks_list avec un message
#     return redirect('stocks_list')

 
