# transactions/context_processors.py
from .models import Producer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.http import urlencode
from django_htmx.http import retarget
from django.db.models import F, ExpressionWrapper, DecimalField, Sum, Q

from transactions.models import Producer, Product, UniqueSector, Country, Province, Client, Supplier
from transactions.forms import ProducerForm
from transactions.filters import ProducerFilter

def header_context(request):
    # Obtenez les données dont vous avez besoin pour le header
    header_data = Producer.objects.filter(user=request.user)  # Remplacez ceci par la logique appropriée
    return {
        'header_data': header_data
    }
