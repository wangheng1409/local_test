# -*- coding: utf-8 -*-

# Scrapy settings for MeituanSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'MeituanSpider'

SPIDER_MODULES = ['MeituanSpider.spiders']
NEWSPIDER_MODULE = 'MeituanSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'MeituanSpider (+http://www.yourdomain.com)'

# LOG_LEVEL = 'INFO'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 25

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 25
CONCURRENT_REQUESTS_PER_IP = 25

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'MeituanSpider.middlewares.MeituanspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'bo_lib.scrapy_tools.BOProxyMiddlewareV2': 543,
   'MeituanSpider.middlewares.ProxyMiddleware': 543,
   'MeituanSpider.middlewares.UAMiddleware': 544,
   'MeituanSpider.middlewares.CustomRetryMiddleware': 545,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'scrapy_redis.pipelines.RedisPipeline': 300,
   'MeituanSpider.pipelines.MeituanspiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
# SCHEDULER_PERSIST = True
#REDIS_START_URLS_AS_SET = False



HEADERS = {'charset': 'utf-8',
           'referer': 'https://servicewechat.com/wx2c348cf579062e56/5/',
           'content-type': 'application/x-www-form-urlencoded',
           'User-Agent': 'MicroMessenger/6.5.6.1020 NetType/WIFI Language/zh_CN',
           'Host': 'wx.waimai.meituan.com',
           'Connection': 'Keep-Alive',
           'Accept-Encoding': 'gzip'}

POI_DATA = {'page_index': '1',
            'navigate_type': '0',
            'category_type': '0',
            'sort_type': '5',
            'page_size': '20',
            'load_type': '1',
            'wm_actual_latitude': '39951660',
            'wm_actual_longitude': '116420500',
            'waimai_sign': '/',
            'wm_appversion': '1.2.2',
            'wm_latitude': '40064695',
            'wm_longitude': '116327513',
            'wm_dversion': '6.5.6',
            'wm_dtype': 'A0001',
            'wm_ctype': 'wxapp'}

MENU_DATA = {
    'wm_poi_id': 1016993,
    'user_id': 3771112,
    'userid': 3771112,
    'wm_actual_latitude': 39951660,
    'wm_actual_longitude': 116420500,
    'waimai_sign': '/',
    'userToken': 'stQe7ScEg8oAb_hRAxnQPpqs-50AAAAAyQMA12345233lSwwpv8a0pSWWWb5xzph-RzfvVHZrHOLQi4xuW_J2cblLzDByqb0bvgHJg',
    'wm_logintoken': 'stQe7ScEg8oAb_hRAxnQPpqs-50AAAAAyQMAAC8Ngg6453524pSWWWb5xzph-RzfvVHZrHOLQi4xuW_J2cblLzDByqb0bvgHJg',
    'wm_appversion': '1.2.2',
    'wm_latitude': 39951660,
    'wm_longitude': 116420500,
    'wm_dversion': '6.5.6',
    'wm_dtype': 'A0001',
    'wm_ctype': 'wxapp'
}

WEB_POI_URL = 'http://waimai.meituan.com/ajax/poilist?_token={}'

WEB_MENU_URL = 'http://waimai.meituan.com/restaurant/{}?pos={}'

WEB_POI_SEARCH_URL = 'https://waimai.meituan.com/geo/geohash?lat={latitude}&lng={longitude}&addr={name}&from=m' #use this url to get geoid

WEB_GEOID_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '__mta=51270422.1490689325385.1490690016537.1490690026457.3; _ga=GA1.3.415372901.1490689325; w_ah="{latitude},{longitude},{name}"',
    'DNT': '1',
    'Host': 'waimai.meituan.com',
    'Origin': 'http://waimai.meituan.com',
    'Referer': 'http://waimai.meituan.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}


WEB_POI_DATA = {
        'classify_type': 'cate_all',
        'sort_type': '0',
        'price_type': '0',
        'support_online_pay': '0',
        'support_invoice': '0',
        'support_logistic': '0',
        'page_offset': '1',
        'page_size': '20'}

WEB_POI_HEADER = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'w_uuid=uRevP84jOdcRSXfLKch6NBZLhrFGK8dXsKZjIY060mm9QxBuToqGF-zhRCfy1Js3; uuid=cf31112345e00399d3.1490103155.0.0.0; w_cid=110101; w_cpy_cn="%E4%B8%9C%E5%9F%8E%E5%8C%BA"; w_cpy=dongchengqu; waddrname="%E4%B8%AD%E5%85%B3%E6%9D%91%E9%9B%8D%E5%92%8C%E8%88%AA%E6%98%9F%E7%A7%91%E6%8A%80%E5%9B%AD-8%E5%8F%B7%E6%A5%BC"; w_geoid=wx4g365fb22z; w_ah="39.95774997398257,116.42728071659803,%E4%B8%AD%E5%85%B3%E6%9D%91%E9%9B%8D%E5%92%8C%E8%88%AA%E6%98%9F%E7%A7%91%E6%8A%80%E5%9B%AD-8%E5%8F%B7%E6%A5%BC"; JSESSIONID=14hgxlicymt2r1xcem7bq6kjtt; _ga=GA1.3.1482810645.1490103092; w_visitid=0a01dda2-bf20-4db4-a9c2-28e0eb418193; __mta=46549400.1490103092603.1490446169753.1490446197804.4; w_utmz="utm_campaign=(direct)&utm_source=(direct)&utm_medium=(none)&utm_content=(none)&utm_term=(none)"',
    'DNT': '1',
    'Host': 'waimai.meituan.com',
    'Origin': 'http://waimai.meituan.com',
    'Referer': 'http://waimai.meituan.com/home/wx4g365fb22z',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}

POI_URL = 'https://wx.waimai.meituan.com/weapp/v1/poi/filter'
MENU_URL = 'https://wx.waimai.meituan.com/weapp/v1/poi/food'

WAP_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '_ga=GA1.2.2129559026.1490150745; _ga=GA1.3.2129559026.1490150745; __mta=155426692.1490150744886.1490955901717.1491367358316.51; w_visitid=51811b31-6b19-42b3-954f-92fe2df3562b; wx_channel_id=0; webp=1; _lxsdk=1512348c2c8-0a880f0d3dbcb-1d3c6853-384000-15b3c97f8c231; w_addr=%E9%9B%8D%E5%92%8C%E5%AE%B6%E5%9B%AD; utm_source=0; w_cid=110100; w_cpy_cn="%E5%8C%97%E4%BA%AC"; w_cpy=beijing; w_latlng=39950516,116420155; JSESSIONID=su9uw51kav0q18wu9r8mv5b9o; _lx_utm=; __mta=155426692.1490150744886.1491367358316.1491370255276.52; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_uuid=jgqb-8yY20WoiRQocGkXBm7bmdkik1fCBwGWNzmSA6ehl2RPDzEV6L9fVG6H9MWY; _lxsdk_s=3ca837a42930b064a14dc11d6440%7C%7C2',
    'DNT': '1',
    'Host': 'i.waimai.meituan.com',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

WAP_POI_DATA = {'page_index': '1',
                'apage': '1'}

WAP_POI_HEADER = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'w_visitid=7fce85e9-17d8-4a8f-b84a-c7b9df707835;',
    'DNT': '1',
    'Host': 'i.waimai.meituan.com',
    'Origin': 'http://i.waimai.meituan.com',
    'Proxy-Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}

WAP_URL = 'http://i.waimai.meituan.com/home?lat={lat}&lng={lng}'
WAP_POI_URL = 'http://i.waimai.meituan.com/ajax/v6/poi/filter?category_type=910&category_text=%E7%BE%8E%E9%A3%9F&_token={token}'
WAP_MENU_URL = 'http://i.waimai.meituan.com/restaurant/{}'
WAP_MENU_POST_URL = 'http://i.waimai.meituan.com/ajax/v8/poi/food?_token={}'


BEIJING_LATITUDE_RANGE = [39666, 40202]
LATITUDE_STEP = 10
LATITUDE_OFFSET = 1000

BEIJING_LONGITUDE_RANGE = [116071, 116687]
LONGITUDE_STEP = 8
LONGITUDE_OFFSET = 3000

#MONGODB_URI = 'mongodb://root:Baiguan2016@60.205.152.167:3717'
MONGODB_URI = 'mongodb://root:Baiguan2016@dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521'
MONGODB_DB = 'Meituan'
MONGODB_POI_COLLECTION = 'POI_BY_BUILDING_REDIS'
MONGODB_MENU_COLLECTION = 'MENU_REDIS'
MONGODB_WEB_POI_COLLECTION = 'POI_WEB'
MONGODB_WEB_MENU_COLLECTION = 'MENU_WEB'
MONGODB_WAP_POI_COLLECTION = 'POI_WAP'
MONGODB_WAP_MENU_COLLECTION = 'WAP_MENU'

REDIS_HOST = 'localhost'
REDIS_PARAMS = {'password': 'bigone2016'}
REDIS_PORT = 6379
REDIS_PASSWORD = 'bigone2016'

# LOG_FILE = 'poiweb.log'


