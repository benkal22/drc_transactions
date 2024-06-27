#transactions/views/suppliers_view.py

from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from ..models import Supplier
from ..serializers import SupplierSerializer

from django.http import JsonResponse
from ..forms import SupplierForm

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    
from django.views.decorators.http import require_POST

def suppliers_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'transactions/suppliers/suppliers_list.html', {'suppliers': suppliers})

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            supplier = form.save()
            return redirect('suppliers_list')
    else:
        form = SupplierForm()
    return render(request, 'transactions/suppliers/supplier_form.html', {'form': form})

def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            return redirect('suppliers_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'transactions/suppliers/supplier_form.html', {'form': form, 'supplier': supplier})

def remove_supplier_confirmation(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'transactions/suppliers/supplier_delete_confirmation.html', {'supplier': supplier})

@require_POST
def remove_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('suppliers_list')
