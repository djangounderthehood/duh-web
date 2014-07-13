from .settings_base import *

import dj_database_url

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'foobar'  # TODO: env var

DATABASES =  {
    'default': dj_database_url.config(),
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_ROOT = 'staticfiles'
