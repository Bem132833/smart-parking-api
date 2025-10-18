from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkingSpotViewSet, ReservationViewSet, PaymentViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'spots', ParkingSpotViewSet, basename='spots')
router.register(r'reservations', ReservationViewSet, basename='reservations')
router.register(r'payments', PaymentViewSet,basename='payments')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

