import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key (hard-coded value)
SECRET_KEY = '76543210abcdefgh'  # Replace this with your actual secret key
if not SECRET_KEY:
    raise ImproperlyConfigured('The SECRET_KEY setting must not be empty.')

print("SECRET_KEY from .env:", SECRET_KEY)

# Debug mode (hard-coded value)
DEBUG = False  # Change to True for development

# CSRF trusted origins (for requests from your Azure web app)
CSRF_TRUSTED_ORIGINS = [
    'https://clipclap-eagsdaaxh5ecaefq.westus-01.azurewebsites.net',
]

# Allowed Hosts (hard-coded value)
ALLOWED_HOSTS = [
    'clipclap-eagsdaaxh5ecaefq.westus-01.azurewebsites.net',
    'localhost',
    '127.0.0.1',
]

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap5',
    # Local apps
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'videos.apps.VideosConfig',
    'django_extensions',
    'interactions.apps.InteractionsConfig',
    'storages',
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'config.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI application configuration
WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration (hard-coded values)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',  # Database name
        'USER': 'israel',  # Database username
        'PASSWORD': 'Nine1122',  # Database password
        'HOST': 'clipclap.postgres.database.azure.com',  # Database host
        'PORT': '5432',  # Database port
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Password validation
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

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (uploads) - Configuring Azure storage for media files
AZURE_STORAGE_ACCOUNT_NAME = 'clipclap'  
AZURE_STORAGE_ACCOUNT_KEY = 'AFYDPBXtquagImz8dI+uvLiVXKBqQ6SBwIl0olTZbgYnTC9hLeHmNmpKfZZRMWhNmwlTrVTThr/w+AStg1m45w=='  # Hard-code the account key here
AZURE_STORAGE_CONTAINER_NAME = 'videos' 

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_CUSTOM_DOMAIN = f'{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net'

# Custom user model
AUTH_USER_MODEL = 'users.CustomUser'

# Login redirect URLs
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# Crispy forms configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

AZURE_STORAGE_ACCOUNT_NAME = 'clipclap'  
AZURE_STORAGE_ACCOUNT_KEY = 'AFYDPBXtquagImz8dI+uvLiVXKBqQ6SBwIl0olTZbgYnTC9hLeHmNmpKfZZRMWhNmwlTrVTThr/w+AStg1m45w==' 
AZURE_STORAGE_CONTAINER_NAME = 'videos'  
