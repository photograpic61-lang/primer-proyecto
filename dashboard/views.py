from django import forms
from .models import Reservation
from datetime import timedelta
from django.core.exceptions import ValidationError

class ReservationForm(forms.ModelForm):
    # Campo extra para la duración que no está directamente en el modelo Reservation,
    # pero que usaremos para calcular el end_time en la vista.
    # Usamos un campo de números para reflejar lo que la plantilla HTML pide.
    duration = forms.IntegerField(
        label="Duración (Horas)",
        min_value=1,
        max_value=24,
        widget=forms.NumberInput(attrs={'class': 'form-control rounded-lg p-2 border-gray-300 shadow-sm', 'placeholder': 'Mínimo 1, Máximo 24'})
    )

    class Meta:
        model = Reservation
        # Excluimos user, parking_location y end_time, ya que serán calculados/asignados en views.py
        fields = ['start_time']

        # Widgets para mejorar la apariencia y funcionalidad del campo de fecha/hora
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control rounded-lg p-2 border-gray-300 shadow-sm',
            }, format='%Y-%m-%dT%H:%M')
        }

    def clean(self):
        """
        Calcula el end_time basado en start_time y duration,
        y lo añade a los datos validados del formulario.
        """
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        duration = cleaned_data.get("duration")

        if start_time and duration is not None:
            # Calcular end_time
            end_time = start_time + timedelta(hours=duration)
            cleaned_data['end_time'] = end_time  # Añadir end_time al diccionario

        return cleaned_data