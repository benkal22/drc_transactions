#transactions/views/producers_view.py

from django.shortcuts import render

from rest_framework import viewsets
from ..models import *
from ..serializers import *

class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
