# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from bo_lib.general import ProxyManager, USER_AGENTS
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from MeituanSpider.util.RedisQueue import RedisQueue
from scrapy import signals
import logging
import base64
import random


logger = logging.getLogger(__name__)


class MeituanspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def __init__(self):
        self.pm = ProxyManager()
        self.proxy_server = "http://proxy.abuyun.com:9020"
        proxy_user = "H4BVZ0310R9EG51D"
        proxy_pass = "7DC2E09E894A4D9E"
        self.proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")

    def process_request(self, request, spider):
        #proxy = self.pm.getProxy()
        # select = random.choice([2])
        # select = 2
        # if select == 1:
        #     request.meta['proxy'] = proxy['https']
        # else:
        request.meta['proxy'] = self.proxy_server
        request.headers["Proxy-Authorization"] = self.proxy_auth


class UAMiddleware(object):
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(USER_AGENTS)


class CustomRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)
        self.retry_queue = RedisQueue()
        self.retry_queue.connect()

    def process_response(self, request, response, spider):
        if 200 != response.status:
            reason = 'redirect {}'.format(response.status)
            return self._retry(request, reason, spider)
        else:
            return response

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        if retries <= self.max_retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request,
                          'retries': retries,
                          'reason': reason},
                         extra={'spider': spider})
            retry_request = request.copy()
            retry_request.meta['retry_times'] = retries
            retry_request.dont_filter = True
            return retry_request
        else:
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request,
                          'retries': retries,
                          'reason': reason},
                         extra={'spider': spider})

            if spider.name == 'Waimai' and request.meta.get('action', '') == 'visit_first_page':
                data = {'name': request.meta['area_name'],
                        'lng': request.meta['longitude'],
                        'lat': request.meta['latitude']}
                try:
                    self.retry_queue.put(spider.name, data)
                except Exception:
                    logger.error('add poi lat-lng info to redis error. the data is: {}'.format(data))

            if spider.name == 'MenuSpider':
                data = {'id': request.meta['id'],
                        'longitude': request.meta['longitude'],
                        'latitude': request.meta['latitude']}
                try:
                    self.retry_queue.put(spider.name, data)
                except Exception:
                    logger.error('add menu lat-lng info to redis error. the data is: {}'.format(data))

