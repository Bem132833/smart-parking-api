from django.test import TestCase
from django.contrib.auth.models import User
from .models import ParkingSpot, Reservation

class ParkingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='1234')
        self.spot = ParkingSpot.objects.create(name="Spot 1", location="Downtown", is_available=True)

    def test_create_reservation(self):
        reservation = Reservation.objects.create(
            user=self.user,
            spot=self.spot,
            start_time="2025-10-18T08:00:00Z",
            end_time="2025-10-18T10:00:00Z"
        )
        self.assertEqual(reservation.spot.name, "Spot 1")
# Create your tests here.
