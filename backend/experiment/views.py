from django.shortcuts import render
from .models import Experiment
from .serializers import ExperimentSerializer

from rest_framework import generics

# Create your views here.


class ExperimentList(generics.ListAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
