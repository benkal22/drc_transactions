#transactions/views/products_view.py

from django.shortcuts import render

from rest_framework import viewsets
from ..models import *
from ..serializers import *

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer