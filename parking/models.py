from django.db import models

class ParkingSpot(models.Model):
    spot_number = models.CharField(max_length=10, unique=True)
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Spot {self.spot_number} - {'Available' if self.is_available else 'Occupied'}"


# Create your models here.
