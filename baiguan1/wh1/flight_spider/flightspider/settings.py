#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'


# Scrapy settings for flightspider project
import os
import logging

PROXY_LIST=[
    [
        'http://123.57.221.137:31009',
        'http://123.57.221.39:31009',
        # 'http://123.57.206.88:31009',
        'http://123.57.206.110:31009',
        'http://101.200.167.203:31009',
        'http://123.57.204.50:31009',
        'http://123.57.221.77:31009',
        'http://112.126.66.123:31009',
        'http://101.200.229.237:31009',
        'http://101.200.232.82:31009',
        'http://101.200.231.4:31009',
        'http://123.57.17.145:31009',
        'http://101.200.231.122:31009',
        'http://123.57.13.246:31009',
        'http://101.200.194.168:31009',
        'http://123.57.17.137:31009',
        'http://123.57.11.60:31009',
        'http://123.57.17.34:31009',
        'http://182.92.4.214:31009',
        'http://101.200.218.54:31009'
    ],
    []
]
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'flightspider'

SPIDER_MODULES = ['flightspider.spiders.ca',
                  'flightspider.spiders.cs',
                  'flightspider.spiders.mu',
                  'flightspider.spiders.jr',
                  'flightspider.spiders.eu',
                  'flightspider.spiders.g5',
                  'flightspider.spiders.mf',
                  'flightspider.spiders.tv',
                  'flightspider.spiders.fu',
                  'flightspider.spiders.ns',
                  'flightspider.spiders.a6',
                  'flightspider.spiders.s_9h',
                  'flightspider.spiders.bk',
                  ]

NEWSPIDER_MODULE = 'flightspider.spiders.cs'

# 爬虫数据库
# DATABASE = {'host': 'rm-m5e2qg7zoobw9x2gi.mysql.rds.aliyuncs.com:3306',
#             'username': 'flight',
#             'password': '2QG7zoob',
#             'database': 'flight'}

DATABASE = {'host': '114.215.144.181:3306',
                 'username': 'flight_test',
                 'password': 'flight_test',
                 'database': 'flight'}

DATABASE_TEST = {'host': '115.28.188.127',
                 'username': 'tt_dev',
                 'password': 'yur140608',
                 'database': 'dev_flight_wh'}

ITEM_PIPELINES = {'flightspider.pipelines.FlightSpiderDetailPipeline': 1,
                  'flightspider.pipelines.FlightSpiderBasePipeline': 2}

# 爬虫请求间隔时间(秒)
# DOWNLOAD_DELAY = 1

# REFERER_ENABLED = False

# 请求超时时间(秒)
DOWNLOAD_TIMEOUT = 30
RETRY_ENABLED=False
LOG_ENABLED = False

LOG_LEVEL = logging.INFO

# log local debug
LOG_TO_REMOTE = False

# LOG_STDOUT = True

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=30
#CONCURRENT_REQUESTS_PER_IP=16

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False


# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'caspider.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'caspider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

# LOG_FILE = "logs/scrapy.log"


RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
RETRY_TIMES = 2

WORKER = 0001

FINAL_TABLE_PATH = os.path.join(PROJECT_DIR, 'huiyou')

# 监控系统(Graphite)
# STATS_CLASS = 'flightspider.statscol.graphite.RedisGraphiteStatsCollector'
# # STATS_CLASS = 'flightspider.statscol.graphite.GraphiteStatsCollector'
#
# # STATS_CLASS = 'scrapygraphite.GraphiteStatsCollector'
# GRAPHITE_HOST = '192.168.122.20'
# GRAPHITE_PORT = 2003
# GRAPHITE_IGNOREKEYS = []
DOWNLOADER_MIDDLEWARES = {
    'flightspider.middlewares.CustomRedirectMiddleware': 500,
}

# 远程日志系统(Sentry)
SENTRY_DSN = 'http://dbeac01f2e5e41779d678797faeee272:4bb0e8a0d14341249356383d3ced59b5@121.42.144.209:9000/3'
SENTRY_DSN_TEST = 'http://6b25dcc763574b45a9483b5c87f447dc:adf733ac1ef9494c9f1169173efd3f1f@192.168.122.30:9000/2'
EXTENSIONS = {
#     # 'scrapy_sentry.extensions.Debug': 2,
#     'scrapy_sentry.extensions.Errors': 1,
      'flightspider.statscol.state_record.SpiderOpenCloseLogging': 800
}

# 代理IP
HTTP_PROXY_HOST = '115.28.234.212:32356'

# 消息队列(Rabbitmq) 相关设置
#RABBITMQ_SERVER = "10.164.0.240"
RABBITMQ_SERVER = "114.215.144.181"
RABBITMQ_SERVER_TEST = "114.215.144.181"
EXCHANGE_DARKMATTER = ""
VHOST_DARKMATTER = "darkmatter"
APP_USER = "test"
APP_PASS = "test123678"

# 部署环境开关
TEST_ENVIRONMENT =True
