from django.urls import path
from .views import ParkingSpotListCreateView

urlpatterns = [
    path('spots/', ParkingSpotListCreateView.as_view(), name='spot-list'),
]
