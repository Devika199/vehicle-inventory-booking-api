
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from datetime import date
from decimal import Decimal

from .models import Vehicle, Booking
from .serializers import VehicleSerializer, BookingSerializer


class VehicleAPI(APIView):

    def get(self, request):
        vehicles = Vehicle.objects.all()

        brand = request.query_params.get('brand')
        fuel_type = request.query_params.get('fuel_type')
        is_available = request.query_params.get('is_available')

        if brand:
            vehicles = vehicles.filter(brand__iexact=brand)

        if fuel_type:
            vehicles = vehicles.filter(fuel_type=fuel_type)

        if is_available is not None:
            if is_available.lower() not in ['true', 'false']:
                return Response(
                    {'error': 'is_available must be true or false'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            vehicles = vehicles.filter(
                is_available=(is_available.lower() == 'true')
            )

        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class VehicleDetailAPI(APIView):

    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    def put(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(
            vehicle,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle.delete()

        return Response(
            {'message': 'Vehicle deleted successfully'},
            status=status.HTTP_200_OK
        )

class BookingAPI(APIView):

    def get(self, request):
        bookings = Booking.objects.select_related('vehicle').all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        vehicle_id = serializer.validated_data['vehicle'].pk

        vehicle = get_object_or_404(
            Vehicle.objects.select_for_update(),
            pk=vehicle_id
        )

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        if not vehicle.is_available:
            return Response(
                {'error': 'This vehicle is unavailable.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        overlapping = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

        if overlapping:
            return Response(
                {'error': 'Vehicle is already booked for these dates.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        days = (end_date - start_date).days
        total_amount = Decimal(days) * vehicle.price_per_day

        booking = serializer.save(total_amount=total_amount)

        vehicle.is_available = False
        vehicle.save(update_fields=['is_available'])

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )


class BookingDetailAPI(APIView):

    def get(self, request, pk):
        booking = get_object_or_404(
            Booking.objects.select_related('vehicle'),
            pk=pk
        )
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
