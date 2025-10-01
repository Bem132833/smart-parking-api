from django.urls import path
from .views import (
    ParkingSpotListCreateView, ParkingSpotDetailView,
    ReservationListCreateView, ReservationDetailView,
    PaymentListCreateView, PaymentDetailView
)

urlpatterns = [
    
    path('spots/', ParkingSpotListCreateView.as_view(), name='spot-list-create'),
    path('spots/<int:pk>/', ParkingSpotDetailView.as_view(), name='spot-detail'),

    
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),

    
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]


