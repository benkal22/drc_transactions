#transactions/views/countries_view.py

from django.shortcuts import render

from rest_framework import viewsets
from ..models import *
from ..serializers import *

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer