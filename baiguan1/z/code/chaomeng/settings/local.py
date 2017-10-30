"""Development settings and globals."""


from os.path import join, normpath
from os import environ
from base import *

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


# DEBUG=False

########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1', '123.112.96.92')

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
########## END TOOLBAR CONFIGURATION

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '//lib.sinaapp.com/js/jquery/2.0.3/jquery-2.0.3.js'
    # 'JQUERY_URL': '//code.jquery.com/jquery-2.0.0.min.js',
}

########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['stylepuzzle.com', 'www.stylepuzzle.com']
########## END SITE CONFIGURATION

# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     'rest_framework.renderers.JSONRenderer',
#     'rest_framework.renderers.BrowsableAPIRenderer'
# )