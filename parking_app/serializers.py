from rest_framework import serializers
from .models import ParkingSpot, Reservation, Payment

class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    spot_detail = ParkingSpotSerializer(source='spot', read_only=True)
    class Meta:
        model = Reservation
        fields = ['id','user','spot','spot_detail','start_time','end_time','total_price','status','created_at']
        read_only_fields = ['id','user','created_at','status']

    def validate(self, data):
        starts = data.get('start_time')
        ends = data.get('end_time')
        if starts and ends and starts >= ends:
            raise serializers.ValidationError("start_time must be before end_time")
        return data

class PaymentSerializer(serializers.ModelSerializer):
    reservation_detail = ReservationSerializer(source='reservation', read_only=True)
    class Meta:
        model = Payment
        fields = ['id','reservation','reservation_detail','amount','payment_method','status','created_at']
        read_only_fields = ['id','created_at']
