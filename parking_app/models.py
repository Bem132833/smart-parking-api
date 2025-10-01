from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ParkingSpot(models.Model):
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[('Available', 'Available'), ('Occupied', 'Occupied'), ('Reserved', 'Reserved')],
        default='Available'
    )
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2,default=10.00)

    def __str__(self):
        return f"Spot {self.id} - {self.location} ({self.status})"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active','active'),('cancelled','cancelled'),('completed','completed')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['spot', 'start_time', 'end_time'])]

    def __str__(self):
        return f"Reservation {self.id} by {self.user.username} for {self.spot}"


class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Card','Card'),('Cash','Cash'),('Mobile','Mobile')])
    status = models.CharField(max_length=20, choices=[('Pending','Pending'),('Completed','Completed'),('Failed','Failed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"



# Create your models here.
