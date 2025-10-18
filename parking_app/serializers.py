from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ParkingSpot, Reservation, Payment

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
     
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class ParkingSpotSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSpot
        # Include actual model fields only + computed fields
        fields = ['id','name','location','number', 'level', 'is_available']

    def get_is_available(self, obj):
        """
        Compute whether the parking spot is available.
        Example: a spot is unavailable if it has an active reservation.
        """
        return not getattr(obj, 'reserved', False)

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    spot_detail = ParkingSpotSerializer(source='spot', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'spot', 'spot_detail',
            'start_time', 'end_time', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'status', 'total_price']

    def validate(self, attrs):
        start = attrs.get('start_time')
        end = attrs.get('end_time')
        if start and end and start >= end:
            raise serializers.ValidationError('start_time must be before end_time')
        return attrs


class PaymentSerializer(serializers.ModelSerializer):
    reservation_detail = ReservationSerializer(source='reservation', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'reservation', 'reservation_detail', 'amount', 'payment_method', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

