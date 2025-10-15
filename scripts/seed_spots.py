import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_parking.settings')
django.setup()

from parking_app.models import ParkingSpot

spots = [
    ('Lot A - 01', 10.0),
    ('Lot A - 02', 10.0),
    ('Lot B - 01', 8.0),
    ('Lot B - 02', 8.0),
    ('Lot C - 01', 5.0),
]
for loc, price in spots:
    ParkingSpot.objects.get_or_create(location=loc, price_per_hour=price)
print("seeded spots")
