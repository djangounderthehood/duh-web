"""
Django settings for duh project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = os.getenv('DJANGO_DEBUG') != 'FALSE'
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    SECRET_KEY = 'hello!'
else:
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['*']

DEBUG_DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///%s' % DEBUG_DB_PATH),
}
DATABASES['default']['CONN_MAX_AGE'] = None


# Application definition

INSTALLED_APPS = (
    'flat',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_gravatar',

    'organizers',
    'sponsors',
    'attendees',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'duh.urls'

WSGI_APPLICATION = 'duh.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
if not DEBUG:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'public')
STATIC_URL = '/static/'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if DEBUG:
    # Use `python -m http.server 8888` from the uploads/ directory to serve
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
    MEDIA_URL = 'http://localhost:8888/'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    EMAIL_HOST = 'smtp.mandrillapp.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    INSTALLED_APPS += (
    'opbeat.contrib.django',
    )
    OPBEAT = {
        'ORGANIZATION_ID': '8ce60e8b722d49ef8b1a67df13377f13',
        'APP_ID': 'f9af431c29',
        'SECRET_TOKEN': os.getenv('OPBEAT_SECRET_TOKEN'),
    }
    MIDDLEWARE_CLASSES = (
        'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    ) + MIDDLEWARE_CLASSES

TITO_AUTH_TOKEN = os.getenv('TITO_AUTH_TOKEN', None)
ADMINS = (('DUtH Team', 'technical@djangounderthehood.com'),)
SERVER_EMAIL = 'hello@djangounderthehood.com'
EMAIL_SUBJECT_PREFIX = '[duth.com] '
