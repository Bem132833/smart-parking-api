from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.utils import timezone
from .models import ParkingSpot, Reservation, Payment
from .serializers import ParkingSpotSerializer, ReservationSerializer, PaymentSerializer

class ParkingSpotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related('spot', 'user').all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        start = serializer.validated_data['start_time']
        end = serializer.validated_data['end_time']
        spot = serializer.validated_data['spot']


        with transaction.atomic():
            overlapping = Reservation.objects.select_for_update().filter(
                spot=spot,
                status='active',
                start_time__lt=end,
                end_time__gt=start
            )
            if overlapping.exists():
                raise serializers.ValidationError("Slot already reserved for requested time window.")

           
            duration_seconds = (end - start).total_seconds()
            duration_hours = duration_seconds / 3600.0
            total_price = round(duration_hours * float(spot.price_per_hour), 2)


            spot.status = 'Reserved'
            spot.save(update_fields=['status'])

            serializer.save(user=user, total_price=total_price, status='active')

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.user != request.user and not request.user.is_staff:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        reservation.status = 'cancelled'
        reservation.save(update_fields=['status'])
        
        overlapping = Reservation.objects.filter(spot=reservation.spot, status='active').exclude(id=reservation.id)
        if not overlapping.exists():
            reservation.spot.status = 'Available'
            reservation.spot.save(update_fields=['status'])
        return Response({'status': 'cancelled'})



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('reservation').all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        reservation = serializer.validated_data['reservation']
        
        if reservation.user != self.request.user and not self.request.user.is_staff:
            raise serializers.ValidationError('Cannot pay for others reservation')
        
        payment = serializer.save(status='Completed')
        reservation.status = 'completed'
        reservation.save(update_fields=['status'])
        return payment


# Create your views here.
