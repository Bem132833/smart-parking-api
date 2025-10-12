from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkingSpotViewSet, ReservationViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'spots', ParkingSpotViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

