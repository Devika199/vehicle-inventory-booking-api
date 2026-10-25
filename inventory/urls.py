
from django.urls import path
from .views import (
    VehicleAPI,
    VehicleDetailAPI,
    BookingAPI,
    BookingDetailAPI,
)

urlpatterns = [
    path('vehicles/', VehicleAPI.as_view(), name='vehicles'),
    path('vehicles/<int:pk>/', VehicleDetailAPI.as_view(),
         name='vehicle-detail'),

    path('bookings/', BookingAPI.as_view(), name='bookings'),
    path('bookings/<int:pk>/', BookingDetailAPI.as_view(),
         name='booking-detail'),
]
