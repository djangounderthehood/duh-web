"""
Django settings for duh project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
import dj_database_url

# Path to the root of the repository
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Basics
DEBUG = os.environ.get('DJANGO_DEBUG', '').lower() != 'false'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'pipeline',
    'debug_toolbar',
    'django_gravatar',
    'opbeat.contrib.django',

    'organizers',
    'sponsors',
    'attendees',
    'tinyblog',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
]

ROOT_URLCONF = 'duh.urls'
WSGI_APPLICATION = 'duh.wsgi.application'

ADMINS = [
    ('DUtH Team', 'technical@djangounderthehood.com'),
]
EMAIL_SUBJECT_PREFIX = '[DUtH] '


# Basic security
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'hello!')
# if not DEBUG:
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Database
DEBUG_DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///%s' % DEBUG_DB_PATH),
}
DATABASES['default']['CONN_MAX_AGE'] = None


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'duh.storages.GzipManifestPipelineStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'public')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)
PIPELINE = {
    'STYLESHEETS': {
        'app': {
            'source_filenames': (
                'css/reset.less',
                'css/style.less',
            ),
            'output_filename': 'css/app.css',
            'extra_context': {
                'media': 'screen,projection',
            },
        },
    },
    'JAVASCRIPT': {
        'app': {
            'source_filenames': (
                'js/main.js',
            ),
            'output_filename': 'js/app.js',
        },
        'vendor': {
            'source_filenames': (
                'js/jquery.countdown.min.js',
                'js/moment.min.js',
                'js/snowfall.jquery.js',
            ),
            'output_filename': 'js/vendor.js',
        },
    },
    'COMPILERS': (
        'pipeline.compilers.less.LessCompiler',
    ),
    'YUGLIFY_BINARY': os.path.join(BASE_DIR, 'node_modules/yuglify/bin/yuglify'),
    'LESS_BINARY': os.path.join(BASE_DIR, 'node_modules/less/bin/lessc'),
}

# Uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'  # Only used in development

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')


# Email
SERVER_EMAIL = 'hello@djangounderthehood.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.mandrillapp.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# Misc
OPBEAT = {
    'ORGANIZATION_ID': '8ce60e8b722d49ef8b1a67df13377f13',
    'APP_ID': '54a01a916c',
    'SECRET_TOKEN': os.environ.get('OPBEAT_SECRET_TOKEN'),
}

TITO_AUTH_TOKEN = os.environ.get('TITO_AUTH_TOKEN')

TINYBLOG_ROOT_DIR = os.path.join(BASE_DIR, 'tinyblog', 'articles')
