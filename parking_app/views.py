from rest_framework import generics
from .models import ParkingSpot
from .serializers import ParkingSpotSerializer

class ParkingSpotListCreateView(generics.ListCreateAPIView):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
from django.shortcuts import render

# Create your views here.
