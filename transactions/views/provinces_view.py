#transactions/views/provinces_view.py

from django.shortcuts import render

from rest_framework import viewsets
from ..models import *
from ..serializers import *

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer