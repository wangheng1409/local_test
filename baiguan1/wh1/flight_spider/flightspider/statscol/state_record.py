#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "fly"

import simplejson
from scrapy import signals
from flightspider import database
from flightspider.lib.http_proxy import relapse_http_proxy


class SpiderOpenCloseLogging(object):
    def __init__(self, crawler):
        self.stats = crawler.stats
        self._dump = crawler.settings.getbool('STATS_DUMP')
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        return ext

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        if self._dump:
            policy_id = spider.task_id
            state = self.stats.get_stats()
            dump = {'start_time': str(state["start_time"]),
                    'finish_time': str(state["finish_time"]),
                    'item_count': self.items_scraped,
                    'finish_reason': state["finish_reason"]
                    }
            # 更新任务状态为以完成
            # 无效航线
            if hasattr(spider, "tmp_retry_times") and spider.tmp_retry_times == -2:
                database.update_task_record(policy_id, simplejson.dumps(dump), 5)
            # 抓取失败
            elif hasattr(spider, "tmp_retry_times") and spider.tmp_retry_times == -1:
                database.update_task_record(policy_id, simplejson.dumps(dump), 4)
            else:
                database.update_task_record(policy_id, simplejson.dumps(dump), 3, self.items_scraped)
                # 释放代理
                relapse_http_proxy(spider.hp_id)

    def item_scraped(self, item, spider):
        self.items_scraped += 1
