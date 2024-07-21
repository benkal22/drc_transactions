#transactions/views/producers_view.py

from django.shortcuts import render

from rest_framework import viewsets
from ..models import Producer
from ..serializers import ProducerSerializer

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.http import require_POST
from transactions.forms import ProducerForm
from django.shortcuts import redirect

class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    
def producers_list(request):
    producers = Producer.objects.all()
    return render(request, 'transactions/producers/producers_list.html', {'producers': producers})

def add_producer(request):
    if request.method == 'POST':
        form = ProducerForm(request.POST, request.FILES)
        if form.is_valid():
            producer = form.save()
            return redirect('producers_list')  # Redirige vers producers_list
        else:
            return render(request, 'transactions/producers/producer_form.html', {'form': form})
    else:
        form = ProducerForm()
    return render(request, 'transactions/producers/producer_form.html', {'form': form})

def edit_producer(request, pk):
    producer = get_object_or_404(Producer, pk=pk)
    if request.method == 'POST':
        form = ProducerForm(request.POST, request.FILES, instance=producer)
        if form.is_valid():
            producer = form.save()
            return redirect('producers_list')  # Redirige vers producers_list
        else:
            return render(request, 'transactions/producers/producer_form.html', {'form': form, 'producer': producer})
    else:
        form = ProducerForm(instance=producer)
    return render(request, 'transactions/producers/producer_form.html', {'form': form, 'producer': producer})

def remove_producer_confirmation(request, pk):
    producer = get_object_or_404(Producer, pk=pk)
    return render(request, 'transactions/producers/producer_delete_confirmation.html', {'producer': producer})

@require_POST
def remove_producer(request, pk):
    producer = get_object_or_404(Producer, pk=pk)
    company_name = producer.company_name  # Pour l'utilisation dans le message de confirmation
    
    producer.delete()
    
    # Redirection vers producers_list avec un message
    return redirect('producers_list')

from django.views.generic import TemplateView

class ProducerListViewSet(TemplateView):
    template_name = "transactions/producers/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['producers'] = Producer.objects.all()
        return context
    
