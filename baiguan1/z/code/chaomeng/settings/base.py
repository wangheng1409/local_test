#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Common settings and globals."""

# from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.utils.translation import ugettext_lazy as _
from os.path import abspath, basename, dirname, join, normpath
from os import environ
from sys import path
import dj_database_url
import os


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION

# PROJECT DIR for EASY-MODE I18L
PROJECT_DIR = os.path.dirname(__file__)

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug

DEBUG = environ.get('DJANGO_DEBUG', False) == 'True'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
# TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Tobias', 'tobias@ichaomeng.com'),
    ('Liming Zhao', 'zhaoliming@ichaomeng.com'),
    ('Tao Li', 'litao@ichaomeng.com'),
    ('Lin Zhang', 'zhanglin@ichaomeng.com'),
    ('Zhang Chi', 'zhangchi@ichaomeng.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
# TIME_ZONE = 'US/Central'
# TIME_ZONE = 'America/Los_Angeles'
TIME_ZONE = 'Asia/Shanghai'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en-us', _('English')),
    ('zh-cn', _('简体中文')),
    # ('zh-tw', _('繁體中文')),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
# SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)
########## END STATIC FILE CONFIGURATION

LOCALE_PATHS = (
    normpath(join(SITE_ROOT, 'locale')),
)


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"nuiux@x(ek_$lt*gmbx)p@j$16b@)-d&c14z2^+l*i@_pr49*0"
########## END SECRET CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

########## END SITE CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.contrib.auth.context_processors.auth',
#     'django.core.context_processors.debug',
#     # 'django.core.context_processors.i18n',
#     'django.core.context_processors.media',
#     'django.core.context_processors.static',
#     'django.core.context_processors.tz',
#     'django.contrib.messages.context_processors.messages',
#     'django.core.context_processors.request',
#     # "allauth.account.context_processors.account",
#     # "allauth.socialaccount.context_processors.socialaccount",
# )

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # allauth specific authentication methods, such as login by e-mail
    # "allauth.account.auth_backends.AuthenticationBackend",
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
# TEMPLATE_DIRS = (
#     normpath(join(SITE_ROOT, 'templates')),
# )
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',

    # 'braces',
    # 'compressor'
    # 'corsheadrs',
    # 'gunicorn'y
    # 'rest_framework',
    # 'rest_framework.authtoken',
    # 'storages',
    # 'djcelery',
    # 'djcelery_email',
    # 'haystack'
    # 'post_office',
)

# Apps specific for this phttps://bitbucket.org/ubernostrum/django-registration/overviewroject go here.
LOCAL_APPS = (
    'user',
    'standard',
    'store',
    'summary',
    'monitor',
    'synclog',
    'advertisement',
    'discovery',
    'custom_model',
    'analytics'
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

########## END APP CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

# Logging settings for django projects, works with django 1.5+
# If DEBUG=True, all logs (including django logs) will be
# written to console and to debug_file.
# If DEBUG=False, logs with level INFO or higher will be
# saved to production_file.
# Logging usage:

# import logging
# logger = logging.getLogger(__name__)
# logger.info("Log this message")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                     '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console':{
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'production_file':{
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'logs/main.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
        },
        'debug_file':{
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'logs/main_debug.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'debug_file', 'production_file'],
            'level': 'INFO',
            'propagate': True
        }

    }
}
########## END LOGGING CONFIGURATION

########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME
########## END WSGI CONFIGURATION

DATABASES['default'] =  dj_database_url.config()


TEMPLATES = [
    {
        'BACKEND': 'django.templates.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.templates.context_processors.debug',
                'django.templates.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.templates.context_processors.i18n',
                'django.templates.context_processors.media',
                'django.templates.context_processors.static',
                'django.templates.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'loaders': [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',
            # ]
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_USER_MODEL = 'user.CMUser'
## Trade DB
TRADE_DB_URL = environ.get('CM_TRADE_DB_URL', '')
BUSSINESS_DB_URL = environ.get('CM_BUSSINESS_DB_URL', '')

TRADE_DB_HOST = environ.get('CM_TRADE_DB_HOST', '')
TRADE_DB_PORT = environ.get('CM_TRADE_DB_PORT', '')
TRADE_DB_NAME = environ.get('CM_TRADE_DB_NAME', '')
TRADE_DB_USERNAME = environ.get('CM_TRADE_DB_USERNAME', '')
TRADE_DB_PASSWORD = environ.get('CM_TRADE_DB_PASSWORD', '')


CM_DB_HOST = environ.get('CM_DB_HOST', '')
CM_DB_USER = environ.get('CM_DB_USER', '')
CM_DB_PASSWORD = environ.get('CM_DB_PASSWORD', '')
CM_DB_NAME = environ.get('CM_DB_NAME', '')

TMALL_ITEM_URL_PREFIX = 'https://detail.tmall.com/item.htm?id='
YHD_ITEM_URL_PREFIX = 'http://item.yhd.com/item/'
FEINIU_ITEM_URL_PREFIX = 'http://item.feiniu.com/'

############# CORS HEADER setting
# if DEBUG:
#     CORS_ORIGIN_WHITELIST = (
#         'cn-test.heypair.com',
#         'localhost:12344',
#         '127.0.0.1:12344',
#         '127.0.0.1:8080',
#     )
# else:
#     CORS_ORIGIN_WHITELIST = (
#         'cn3.heypair.com',
#         'heypair.com',
#         'goshippo.com',
#         'stylepuzzle.com',
#     )
