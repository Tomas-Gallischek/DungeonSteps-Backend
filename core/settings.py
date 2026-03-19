import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Načtení proměnných z .env souboru
load_dotenv()

# Cesta k projektu
BASE_DIR = Path(__file__).resolve().parent.parent

# --- BEZPEČNOST ---
# Na Renderu si nastav vlastní SECRET_KEY v Environment Variables
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-zmente-v-produkci')

# DEBUG je True lokálně, na Renderu nastav proměnnou DEBUG na False
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Povolíme lokální host i tvou budoucí adresu na Renderu
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
if os.getenv('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.getenv('RENDER_EXTERNAL_HOSTNAME'))


# --- APLIKACE ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Knihovny třetích stran
    'rest_framework.authtoken', # Povolí generování tokenů
    'rest_framework',
    'corsheaders',      # Důležité pro komunikaci s Kivy
    'whitenoise.runserver_nostatic', # Vylepšený vývojový server pro statiku
    
    # Tvoje aplikace

    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Musí být hned pod security
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',      # Musí být nad CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# --- DATABÁZE ---
# Automaticky použije DATABASE_URL z .env (lokálně) nebo z Renderu (produkce)
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# --- VALIDACE HESEL ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- LOCALIZACE ---
LANGUAGE_CODE = 'cs' # Nastaveno na češtinu
TIME_ZONE = 'Europe/Prague'
USE_I18N = True
USE_TZ = True


# --- STATICKÉ SOUBORY ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise konfigurace pro efektivní ukládání a kompresi
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- API A CORS NASTAVENÍ ---
# Povolíme přístup z mobilní aplikace (pro vývoj povolujeme vše)
CORS_ALLOW_ALL_ORIGINS = True 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # V základu bude vše zamčené
    ],
}