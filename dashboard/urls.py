from django.contrib import admin
from django.urls import path
from dashboard.views import HomeView, CreateReservationView # Importamos la nueva vista

urlpatterns = [
    path('admin/', admin.site.urls),
    # URL de la página principal
    path('', HomeView.as_view(), name='home'), 
    # URL para crear una reserva, acepta el ID del aparcamiento (integer)
    path('reserve/<int:parking_id>/', CreateReservationView.as_view(), name='create_reservation'), 
]
