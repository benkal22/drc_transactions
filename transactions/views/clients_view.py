from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from rest_framework import viewsets, generics
from transactions.forms import ClientForm
from transactions.models import Client
from transactions.serializers import ClientSerializer

from rest_framework.generics import ListAPIView

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientListAPIView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

def clients_list(request):
    clients = Client.objects.all()
    return render(request, 'transactions/clients/clients_list.html', {'clients': clients})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm()
    return render(request, 'transactions/clients/client_form.html', {'form': form})

def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'transactions/clients/client_form.html', {'form': form, 'client': client})

def remove_client_confirmation(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'transactions/clients/client_delete_confirmation.html', {'client': client})

@require_POST
def remove_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('clients_list')
