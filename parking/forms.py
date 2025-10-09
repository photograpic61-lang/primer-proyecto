from django import forms
from .models import ParkingLocation, Reservation
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

# Definimos el formato esperado para la entrada HTML5 de fecha y hora local
INPUT_DATETIME_FORMATS = ['%Y-%m-%dT%H:%M']

class ReservationForm(forms.ModelForm):
    # Campo para seleccionar la ubicación. Se llena dinámicamente en __init__.
    parking_location = forms.ChoiceField(
        label="Seleccionar Ubicación",
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'})
    )

    start_time = forms.DateTimeField(
        input_formats=INPUT_DATETIME_FORMATS,
        label="Hora de Inicio",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    end_time = forms.DateTimeField(
        input_formats=INPUT_DATETIME_FORMATS,
        label="Hora de Finalización",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Reservation
        fields = ['parking_location', 'start_time', 'end_time']

    def __init__(self, *args, parking_locations=None, **kwargs):
        super().__init__(*args, **kwargs)
        if parking_locations:
            # Llenamos las opciones del campo Location con ID y nombre/precio.
            choices = [(loc.id, f"{loc.name} (${loc.hourly_price}/h)") for loc in parking_locations]
            self.fields['parking_location'].choices = choices
            # Aseguramos que el valor retornado sea un entero (el ID de la ubicación)
            self.fields['parking_location'].coerce = int

    def clean(self):
        """
        Realiza validaciones críticas:
        1. Valida que los tiempos sean lógicos (futuro, inicio < fin).
        2. Verifica que haya capacidad disponible para el rango de tiempo seleccionado.
        """
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        location_id = cleaned_data.get("parking_location")

        # 1. Validación de Tiempos
        if start_time and end_time:
            # El tiempo de inicio debe ser estrictamente posterior al momento actual
            if start_time <= timezone.now():
                raise forms.ValidationError("La hora de inicio debe ser posterior al momento actual.")
            
            # El tiempo de fin debe ser estrictamente posterior al de inicio
            if end_time <= start_time:
                raise forms.ValidationError("La hora de finalización debe ser posterior a la hora de inicio.")
        
        # 2. Validación de Disponibilidad (Solapamiento)
        if location_id:
            try:
                location = ParkingLocation.objects.get(pk=location_id)
            except ParkingLocation.DoesNotExist:
                raise forms.ValidationError("Ubicación seleccionada no es válida.")

            # Contamos las reservas que se solapan con el nuevo rango [start_time, end_time]
            # Un solapamiento existe si:
            # - La reserva existente termina DESPUÉS de nuestro inicio (start_time__lt=end_time)
            # - Y la reserva existente empieza ANTES de nuestro fin (end_time__gt=start_time)
            overlapping_reservations_count = Reservation.objects.filter(
                parking_location=location,
                start_time__lt=end_time, 
                end_time__gt=start_time, 
            ).count()

            # Verificamos si la capacidad total de la ubicación es excedida
            if overlapping_reservations_count >= location.total_spots:
                raise forms.ValidationError(f"Lo sentimos, no hay puestos disponibles en {location.name} para ese horario. Capacidad: {location.total_spots}")
                
            # Adjuntamos el objeto Location (no solo el ID) a los datos limpios 
            # para que la vista lo use directamente al guardar.
            cleaned_data['parking_location'] = location

        return cleaned_data
