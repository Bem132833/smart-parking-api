from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


# ------------------------------
# Parking Spot Model
# ------------------------------
class ParkingSpot(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    level = models.CharField(max_length=50, blank=True, null=True)  # <-- added to match serializer
    status = models.CharField(
        max_length=20,
        choices=[
            ('Available', 'Available'),
            ('Occupied', 'Occupied'),
            ('Reserved', 'Reserved'),
        ],
        default='Available'
    )
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)

    class Meta:
        verbose_name = "Parking Spot"
        verbose_name_plural = "Parking Spots"
        ordering = ['location', 'number']

    def __str__(self):
        return f"{self.name or f'Spot {self.number}'} - {self.location} ({self.status})"

    @property
    def is_available(self):
        """Boolean shortcut for availability."""
        return self.status == 'Available'


# ------------------------------
# Reservation Model
# ------------------------------
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('cancelled', 'Cancelled'),
            ('completed', 'Completed'),
        ],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['spot', 'start_time', 'end_time'])]
        ordering = ['-created_at']

    def __str__(self):
        return f"Reservation {self.id} | {self.user.username} | {self.spot.name or self.spot.number}"

    def clean(self):
        """Prevent overlapping bookings."""
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")
        overlapping = Reservation.objects.filter(
            spot=self.spot,
            end_time__gt=self.start_time,
            start_time__lt=self.end_time,
        ).exclude(id=self.id)
        if overlapping.exists():
            raise ValidationError("This spot is already booked for that time range.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# ------------------------------
# Payment Model
# ------------------------------
class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('Card', 'Card'),
            ('Cash', 'Cash'),
            ('MobileMoney', 'Mobile Money'),
        ],
        default='Card',
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed'),
        ],
        default='Pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} | {self.reservation.user.username} | {self.status}"



# Create your models here.
