from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 

# =====================================================================
# Modelo: ParkingLocation (Ubicaciones disponibles para reservar)
# =====================================================================
class ParkingLocation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de la Ubicación")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitud")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitud")
    hourly_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Precio por Hora (USD)")
    total_spots = models.IntegerField(verbose_name="Capacidad Total")

    @property
    def available_spots(self):
        """Calcula el número de puestos libres AHORA mismo."""
        # Contar reservas activas (aquellas cuyo end_time es posterior al tiempo actual)
        active_reservations = self.reservations.filter(
            end_time__gt=timezone.now()
        ).count()
        return self.total_spots - active_reservations

    @property
    def is_available(self):
        """Devuelve True si hay al menos un lugar disponible ahora."""
        return self.available_spots > 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ubicación de Estacionamiento"
        verbose_name_plural = "Ubicaciones de Estacionamiento"

# =====================================================================
# Modelo: Reservation (Reservas realizadas)
# =====================================================================
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name="Usuario")
    parking_location = models.ForeignKey(ParkingLocation, on_delete=models.CASCADE, related_name='reservations', verbose_name="Ubicación")
    start_time = models.DateTimeField(verbose_name="Hora de Inicio")
    end_time = models.DateTimeField(verbose_name="Hora de Fin")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return f"Reserva de {self.user.username} en {self.parking_location.name}"

    @property
    def is_active(self):
        """Verifica si la reserva está activa en el momento actual."""
        now = timezone.now()
        return self.start_time <= now and self.end_time > now

    class Meta:
        ordering = ['start_time']
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
