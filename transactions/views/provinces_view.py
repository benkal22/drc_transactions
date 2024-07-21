#transactions/views/provinces_view.py

from django.shortcuts import render

from rest_framework import viewsets
from ..models import *
from ..serializers import *

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

from django.http import JsonResponse

def load_provinces(request):
    country_id = request.GET.get('country_id')
    provinces = Province.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(provinces), safe=False)