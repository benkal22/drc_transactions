from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from rest_framework import viewsets, generics
from transactions.forms import ClientForm
from transactions.serializers import ClientSerializer

from rest_framework.generics import ListAPIView

from django.views.generic import TemplateView
from ..models import Client, Country, Province, Product, UniqueSector

from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.views import View

from django.db import IntegrityError, transaction


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientListAPIView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientListView(View):
    template_name = "transactions/clients/manage_client.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        if request.htmx:
            return render(request, "transactions/clients/partials/client_list.html", context)
        return render(request, self.template_name, context)

    def get_context_data(self, request):
        context = {}
        clients_list = Client.objects.all().order_by('id') 
        total_sales = sum(client.total_sales for client in clients_list)
        average_price = total_sales / len(clients_list) if clients_list else 0

        paginator = Paginator(clients_list, self.paginate_by)
        page_number = request.GET.get('page')
        clients = paginator.get_page(page_number)

        context['clients'] = clients
        context['total_sales'] = total_sales
        context['average_price'] = average_price
        context['sectors'] = UniqueSector.objects.all()
        context['products'] = Product.objects.all()
        context['countries'] = Country.objects.all()
        context['provinces'] = Province.objects.all()
        context['form'] = ClientForm()  # Ajouter le formulaire ici
        
        return context 

class ClientCreateView(View):
    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"Client '{client.name or client.company_name}' ajouté avec succès.")
            # messages.clear(request)
            if request.htmx:
                return self.refresh_client_list(request)
            return redirect('transactions:client_list')
            
        else:
            context = ClientListView().get_context_data(request)
            context['form'] = form
            if request.htmx:
                return render(request, "transactions/clients/partials/client_form.html", context)
            return render(request, "transactions/clients/manage_client.html", context)

    def refresh_client_list(self, request):
        context = ClientListView().get_context_data(request)
        return render(request, "transactions/clients/partials/client_list.html", context)

class ClientEditView(View):
    def get(self, request, *args, **kwargs):
        client = get_object_or_404(Client, id=kwargs['client_id'])
        form = ClientForm(instance=client)
        context = {'form': form, 'edit_client': client}
        return render(request, 'transactions/clients/partials/client_form.html', context)

    def post(self, request, *args, **kwargs):
        client = get_object_or_404(Client, id=kwargs['client_id'])
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f"Client '{client.name}' mis à jour avec succès.")
            # messages.clear(request)
            return ClientCreateView().refresh_client_list(request)
        else:
            context = {'form': form, 'edit_client': client}
            return render(request, 'transactions/clients/partials/client_form.html', context)

class ClientDeleteView(View):
    def post(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        try:
            client = get_object_or_404(Client, pk=client_id)
            client.delete()
            messages.success(request, f"Client '{client.name or client.company_name}' supprimé avec succès.")
        except Client.DoesNotExist:
            messages.error(request, "Le client que vous essayez de supprimer n'existe pas.")
            messages.clear(request)
        if request.htmx:
            return ClientCreateView().refresh_client_list(request)
        return redirect('transactions:client_list')

class MessagesPartialView(View):
    def get(self, request, *args, **kwargs):
        context = {'messages': messages.get_messages(request)}
        return render(request, "transactions/clients/partials/messages.html", context)
