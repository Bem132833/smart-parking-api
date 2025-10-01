from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import ParkingSpot, Reservation, Payment
from .serializers import ParkingSpotSerializer, ReservationSerializer, PaymentSerializer


class ParkingSpotListCreateView(generics.ListCreateAPIView):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer

class ParkingSpotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.select_related('spot','user').all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        
        user = self.request.user
        starts = serializer.validated_data['start_time']
        ends = serializer.validated_data['end_time']
        spot = serializer.validated_data['spot']

        
        with transaction.atomic():
            overlapping = Reservation.objects.select_for_update().filter(
                spot=spot,
                status='active',
                start_time__lt=ends,
                end_time__gt=starts
            )
            if overlapping.exists():
                raise serializers.ValidationError("This spot is already reserved for the requested time range.")
            
            duration_hours = (ends - starts).total_seconds() / 3600.0
            total_price = round(duration_hours * float(spot.price_per_hour), 2)
            serializer.save(user=user, total_price=total_price, status='active')

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.select_related('reservation').all()
    serializer_class = PaymentSerializer

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# Create your views here.
