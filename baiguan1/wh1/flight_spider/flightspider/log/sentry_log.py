#! /usr/bin/env python
# coding:utf-8

import logging
from logging import config
from flightspider import settings

if settings.TEST_ENVIRONMENT:
    DSN = settings.SENTRY_DSN_TEST
else:
    DSN = settings.SENTRY_DSN

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        # 'sentry': {
        #     'level': 'DEBUG',  # (这里改为DEBUG，类似于logging里面限制日志等级的功能)
        #     'class': 'raven.handlers.logging.SentryHandler',
        #     'dsn': DSN,
        # },
    },

    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


logging.config.dictConfig(LOGGING)
log = logging.getLogger(__name__)
#
# def log_msg():
#     logging.config.dictConfig(LOGGING)
#     print __name__
#     logger = logging.getLogger(__name__)
#     return logger

if __name__ == "__main__":
    log.info("Test sentry ...")
