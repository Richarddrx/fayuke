from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    '.vercel.app',
    '.europe58.com',
    'europe58.com',
    '127.0.0.1',
    'localhost',
]

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://europe58.com',
    'https://www.europe58.com',
]

# Static files — collected during Vercel build
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files — use external storage in production
MEDIA_ROOT = BASE_DIR / 'media'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'WARNING'},
}
