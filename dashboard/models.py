from django.db import models
from django.conf import settings # IMPORTACIÓN NECESARIA
# Eliminamos: from django.contrib.auth.models import User

class ParkingLocation(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    hourly_price = models.DecimalField(max_digits=6, decimal_places=2)
    total_spots = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    # CORRECCIÓN CLAVE: Usar settings.AUTH_USER_MODEL para la referencia
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    parking_location = models.ForeignKey(ParkingLocation, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.parking_location.name}"

    def save(self, *args, **kwargs):
        """Actualizamos disponibilidad al guardar"""
        super().save(*args, **kwargs)
        active_reservations = Reservation.objects.filter(
            parking_location=self.parking_location,
            end_time__gt=self.start_time, # Usar __gt para evitar contar la misma reserva
            start_time__lt=self.end_time
        ).exclude(pk=self.pk) # Excluye la reserva actual para evitar bucles
        
        # Corrección: El save() del modelo no debería modificar otro modelo directamente
        # a menos que sea necesario. Pero manteniendo tu lógica:
        self.parking_location.is_available = not active_reservations.exists()
        self.parking_location.save()
