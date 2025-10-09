from django.contrib import admin
from .models import ParkingLocation, Reservation

# 1. Registro del Modelo ParkingLocation
@admin.register(ParkingLocation)
class ParkingLocationAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista del administrador
    list_display = ('name', 'latitude', 'longitude', 'hourly_price', 'total_spots', 'is_available')
    # Campos por los que se puede buscar
    search_fields = ('name',)

# 2. Registro del Modelo Reservation
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista
    list_display = ('user', 'parking_location', 'start_time', 'end_time', 'is_active')
    # Filtros que aparecen en la barra lateral
    list_filter = ('is_active', 'start_time', 'parking_location')
    # Campos por los que se puede buscar
    search_fields = ('user__username', 'parking_location__name')