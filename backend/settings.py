from pathlib import Path
from datetime import timedelta
from rest_framework.settings import api_settings
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

envFile = os.environ.get("ENV_FILE_NAME", ".env")
load_dotenv(envFile)


# ──────────────────────────────────────────────
# SECURITY
# ──────────────────────────────────────────────

SECRET_KEY = 'django-insecure-tmyu%qin7lw6zi#mni9fl)()58ltzxj2*ye_=s5#y2gqcp8#@2'

DEBUG = True

ALLOWED_HOSTS = ['*']


# ──────────────────────────────────────────────
# APPLICATION
# ──────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'knox',
    'business',
    'axes',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]



ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'client' / 'dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

STATICFILES_DIRS = (
    BASE_DIR.joinpath('client', 'dist'),
)   


# ──────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────

dbname = str(os.getenv("POSTGRES_DB"))
dbhost = str(os.getenv("POSTGRES_HOST"))
dbport = str(os.getenv("POSTGRES_PORT"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.getenv("POSTGRES_DB")),
        "USER": str(os.getenv("POSTGRES_USER")),
        "PASSWORD": str(os.getenv("POSTGRES_PSW")),
        "HOST": str(os.getenv("POSTGRES_HOST")),
        "PORT": str(os.getenv("POSTGRES_PORT")),
    }
}

AUTH_USER_MODEL = 'business.UserProfile'

# ──────────────────────────────────────────────
# PASSWORD VALIDATION
# ──────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ──────────────────────────────────────────────
# INTERNATIONALISATION
# ──────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ──────────────────────────────────────────────
# STATIC & MEDIA FILES
# ──────────────────────────────────────────────

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ──────────────────────────────────────────────
# REST FRAMEWORK & KNOX
# ──────────────────────────────────────────────

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  
    ],
}

KNOX_TOKEN_MODEL = 'knox.AuthToken'

REST_KNOX = {
  'SECURE_HASH_ALGORITHM': 'hashlib.sha512',
  'AUTH_TOKEN_CHARACTER_LENGTH': 64,
  'TOKEN_TTL': timedelta(hours=3),
  'USER_SERIALIZER': 'knox.serializers.UserSerializer',
  'TOKEN_LIMIT_PER_USER': None,
  'AUTO_REFRESH': False,
  'AUTO_REFRESH_MAX_TTL': None,
  'MIN_REFRESH_INTERVAL': 60,
  'AUTH_HEADER_PREFIX': 'Token',
  'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
  'TOKEN_MODEL': 'knox.AuthToken',
}  

# ──────────────────────────────────────────────
# AXES
# ──────────────────────────────────────────────

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_FAILURE_LIMIT = 20
AXES_COOLOFF_TIME = 1

# ──────────────────────────────────────────────
# CORS & CSRF
# ──────────────────────────────────────────────

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False  
CSRF_COOKIE_NAME = 'csrftoken'

SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False