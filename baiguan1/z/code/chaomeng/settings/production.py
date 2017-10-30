# -*- coding: utf-8 -*-

"""Production settings and globals."""


from os import environ
from base import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
# EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
# EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
# EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'info@stylepuzzle.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
# EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
# EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
# EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
# SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION

########## DATABASE CONFIGURATION
# DATABASES = {}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECRET_KEY = get_env_setting('DJANGO_SECRET_KEY')
########## END SECRET CONFIGURATION

# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     'rest_framework.renderers.JSONRenderer',
# )


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['b.ichaomeng.com', '54.222.208.68', 'tobias.ichaomeng.com', 'ads.ichaomeng.com']
########## END SITE CONFIGURATION

############# S3
# allow static to sync, otherwise, it will overwrite
# AWS_PRELOAD_METADATA = True

# DEFAULT_FILE_STORAGE = 'core.s3utils.MediaRootS3BotoStorage'
# STATICFILES_STORAGE = 'core.s3utils.StaticRootS3BotoStorage'
# DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage'
# STATICFILES_STORAGE = 'qiniustorage.backends.QiniuStaticStorage'

# AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = get_env_setting('AWS_STORAGE_BUCKET_NAME')
# AWS_QUERYSTRING_AUTH = False

# CLOUDFRONT_URL = '%s.cloudfront.net' % get_env_setting('AWS_CLOUDFRONT_NAME')

############# END S3
# allow static to sync, otherwise, it will overwrite
AWS_PRELOAD_METADATA = True
 
DEFAULT_FILE_STORAGE = 'core.s3utils.MediaRootS3BotoStorage'
# Un comment the following if you need static file in S3 as well.
# STATICFILES_STORAGE = 'core.s3utils.StaticRootS3BotoStorage'
 
 
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST="s3.cn-north-1.amazonaws.com.cn"
 
# CLOUDFRONT_URL = '%s.cloudfront.net' % get_env_setting('AWS_CLOUDFRONT_NAME')
S3_URL = 's3.cn-north-1.amazonaws.com.cn/%s' % AWS_STORAGE_BUCKET_NAME

DEFAULT_CHARSET = 'utf-8'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.exmail.qq.com'                   #SMTP地址
EMAIL_PORT = 25                                 #SMTP端口
EMAIL_HOST_USER = 'alert@ichaomeng.com'       
EMAIL_HOST_PASSWORD = environ.get('CM_EMAIL_HOST_PASSWORD')             
EMAIL_SUBJECT_PREFIX = u'[超盟]'            #为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True                             #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 5
EMAIL_SSL_KEYFILE = None
EMAIL_SSL_CERTFILE = None
DEFAULT_FROM_EMAIL = u'超盟 <alert@ichaomeng.com>'

SERVER_EMAIL = '超盟 <alert@ichaomeng.com>'   
