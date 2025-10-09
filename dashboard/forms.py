from django import forms
from .models import Reservation
from datetime import datetime

# Definimos el formato esperado para el campo de entrada (importante para datetime-local)
INPUT_DATETIME_FORMATS = [
    '%Y-%m-%dT%H:%M',  # Formato HTML5 estándar
]

class ReservationForm(forms.ModelForm):
    """
    Formulario para la creación de una reserva.
    Solo pedimos los tiempos; el usuario y la ubicación se añaden en la vista.
    """
    start_time = forms.DateTimeField(
        input_formats=INPUT_DATETIME_FORMATS,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    end_time = forms.DateTimeField(
        input_formats=INPUT_DATETIME_FORMATS,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Reservation
        # SOLO pedimos start_time y end_time
        fields = ['start_time', 'end_time']

    def clean(self):
        """
        Validación a nivel de formulario:
        1. Asegurar que start_time es posterior al tiempo actual.
        2. Asegurar que end_time es posterior a start_time.
        """
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            # 1. start_time debe ser futuro
            if start_time <= datetime.now():
                raise forms.ValidationError("La hora de inicio debe ser posterior al momento actual.")

            # 2. end_time debe ser posterior a start_time
            if end_time <= start_time:
                raise forms.ValidationError("La hora de finalización debe ser posterior a la hora de inicio.")

        return cleaned_data
