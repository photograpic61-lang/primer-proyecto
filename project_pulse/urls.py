from django.contrib import admin
from django.urls import path, include 

# Este archivo ya no importa nada de dashboard.views, lo cual resuelve el error.

urlpatterns = [
    # 1. Panel de Administración de Django
    path('admin/', admin.site.urls),
    
    # 2. Rutas de Autenticación (login, logout, etc. para usar el decorador @login_required)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 3. La URL Raíz (/) se dirige a la aplicación 'parking'
    path('', include('parking.urls')),
]
