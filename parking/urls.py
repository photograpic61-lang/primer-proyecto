from django.urls import path
from . import views

# El nombre de la aplicación es crucial para la función reverse en las vistas
app_name = 'parking'

urlpatterns = [
    # Ruta principal: Muestra el dashboard con mapa, tarjetas y formulario.
    path('', views.index, name='index'),
    
    # Ruta para procesar la reserva (solo POST)
    # Esta URL no se accede directamente por el navegador, se usa en el action del formulario.
    path('reserve/', views.reserve, name='reserve'),
]
