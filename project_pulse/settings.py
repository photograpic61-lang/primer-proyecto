from pathlib import Path

# Configuración del Directorio Base
BASE_DIR = Path(__file__).resolve().parent.parent

# ¡IMPORTANTE! Reemplaza 'tu-clave-secreta-aqui' con una cadena larga y aleatoria
SECRET_KEY = 'tu-clave-secreta-aqui'
DEBUG = False

# Hosts permitidos para PythonAnywhere
ALLOWED_HOSTS = ['aparcamiento.pythonanywhere.com', '127.0.0.1', 'localhost']

# ... código anterior ...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🚨 ¡ESTA LÍNEA ES LA CLAVE! 🚨
    'parking',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ... (deja todo lo demás igual)

# Rutas de las plantillas (simplificadas para buscar solo dentro de las aplicaciones)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [], # ¡Eliminar la búsqueda global para evitar conflictos!
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ... (deja todo lo demás igual)


# Configuración de URLs y WSGI
ROOT_URLCONF = "project_pulse.urls"
WSGI_APPLICATION = "project_pulse.wsgi.application"

# Base de datos SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de estáticos para producción en PythonAnywhere
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Puedes añadir el resto de configuraciones (AUTH_PASSWORD_VALIDATORS, LANGUAGE_CODE, etc.)
# al final, pero este bloque es suficiente para el despliegue.
# --- CÓDIGO EXISTENTE ARRIBA ---
# ... (otras configuraciones)

# Redirección después de iniciar sesión
LOGIN_REDIRECT_URL = '/'  # Redirige a la página principal ('home')
# URL a la que se redirige si un usuario no está autenticado (para la vista de reserva)
LOGIN_URL = '/accounts/login/'

# --- AÑADE ESTAS LÍNEAS AL FINAL ---
