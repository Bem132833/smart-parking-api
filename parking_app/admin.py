from django.contrib import admin
from .models import ParkingSpot, Reservation, Payment

admin.site.register(ParkingSpot)
admin.site.register(Reservation)
admin.site.register(Payment)
# Register your models here.
