#transactions/views/clients_view.py

from django.shortcuts import render

from rest_framework import viewsets
from ..models import Client
from ..serializers import ClientSerializer

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.http import require_POST
from transactions.forms import ClientForm
from django.shortcuts import redirect

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    
def clients_list(request):
    clients = Client.objects.all()
    return render(request, 'transactions/clients/clients_list.html', {'clients': clients})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save()
            return redirect('clients_list')  # Redirige vers clients_list
        else:
            return render(request, 'transactions/clients/client_form.html', {'form': form})
    else:
        form = ClientForm()
    return render(request, 'transactions/clients/client_form.html', {'form': form})

def edit_client(request, pk):
    client = get_object_or_404(client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            client = form.save()
            return redirect('clients_list')  # Redirige vers clients_list
        else:
            return render(request, 'transactions/clients/client_form.html', {'form': form, 'client': client})
    else:
        form = ClientForm(instance=client)
    return render(request, 'transactions/clients/client_form.html', {'form': form, 'client': client})

def remove_client_confirmation(request, pk):
    client = get_object_or_404(client, pk=pk)
    return render(request, 'transactions/clients/client_delete_confirmation.html', {'client': client})

@require_POST
def remove_client(request, pk):
    client = get_object_or_404(client, pk=pk)
    name = client.name  # Pour l'utilisation dans le message de confirmation
    
    client.delete()
    
    # Redirection vers clients_list avec un message
    return redirect('clients_list')


