from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import json

from .models import ParkingLocation, Reservation
from .forms import ReservationForm

def index(request):
    """Muestra el dashboard principal con el mapa y la lista de ubicaciones."""
    
    # Obtener todas las ubicaciones de estacionamiento
    locations = ParkingLocation.objects.all()
    
    # Serializar los datos de ubicación (incluyendo propiedades) para JavaScript (Leaflet Map)
    locations_data = []
    for loc in locations:
        locations_data.append({
            'name': loc.name,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'hourly_price': float(loc.hourly_price),
            'total_spots': loc.total_spots,
            # Las propiedades calculadas son esenciales aquí:
            'available_spots': loc.available_spots, 
            'is_available': loc.is_available,
        })
    
    locations_json = json.dumps(locations_data)
    
    # Inicializar el formulario de reserva
    form = ReservationForm(locations=locations) 

    context = {
        'locations': locations,
        'locations_json': locations_json,
        'form': form,
    }
    return render(request, 'parking/index.html', context)


@login_required
def reserve(request):
    """Maneja el envío del formulario de reserva."""
    
    locations = ParkingLocation.objects.all()
    
    if request.method == 'POST':
        # Instanciamos el formulario, asegurándonos de pasarle las ubicaciones
        form = ReservationForm(request.POST, locations=locations) 
        
        if form.is_valid():
            # 1. Asignar los campos faltantes (user y location)
            reservation = form.save(commit=False)
            reservation.user = request.user
            
            # La ubicación ya está en cleaned_data gracias a la lógica del formulario
            parking_location = form.cleaned_data.get('parking_location')
            reservation.parking_location = parking_location
            
            # 2. Asignar los tiempos
            reservation.start_time = form.cleaned_data['start_time']
            reservation.end_time = form.cleaned_data['end_time']
            
            reservation.save()
            
            # Mensaje de éxito
            messages.success(request, f"Reserva confirmada en {parking_location.name} desde {reservation.start_time.strftime('%H:%M')} hasta {reservation.end_time.strftime('%H:%M')}.")
            
            return redirect('parking:index')
        else:
            # Si el formulario no es válido (ej. solapamiento de tiempo), mostramos los errores
            messages.error(request, "Error al procesar la reserva. Por favor, revise los errores del formulario.")
            
            # Renderizamos la página principal con el formulario no válido para mostrar errores.
            context = {
                'locations': locations,
                'locations_json': json.dumps([
                    {
                        'name': loc.name, 'latitude': loc.latitude, 'longitude': loc.longitude, 
                        'hourly_price': float(loc.hourly_price), 'total_spots': loc.total_spots,
                        'available_spots': loc.available_spots, 'is_available': loc.is_available
                    } for loc in locations
                ]),
                'form': form,
            }
            return render(request, 'parking/index.html', context)
    
    # Si alguien intenta acceder a /reserve/ directamente con GET, lo redirigimos
    return redirect('parking:index')