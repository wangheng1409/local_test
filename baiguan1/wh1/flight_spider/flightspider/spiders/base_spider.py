#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

from flightspider import database
from flightspider import settings
from scrapy.spiders import Spider
from scrapy.exceptions import CloseSpider
from flightspider.log.sentry_log import log
from flightspider.lib import http_proxy


class BaseSpider(Spider):
    task_id = -1
    http_proxy = ""
    hp_id = -1
    tmp_retry_times = 0
    ipindex = ''

    def __init__(self, task_id=None, ipindex=None):
        # raise CloseSpider('')
        if task_id:
            self.task_id = task_id
        if ipindex:
            self.ipindex = ipindex
        try:
            self.http_proxy, self.hp_id = http_proxy.get_http_proxy(self.code)
        except Exception as e:
            self.logger.warning(e)

    def get_tasks(self, company):
        """
        根据配置文件worker获取从抓取策略获取任务
        :param company:
        :return:
        """
        if self.task_id == -1:
            tasks = database.get_tasks(settings.WORKER, self.name, company)
        else:
            tasks = database.get_tasks("", "", "", self.task_id)
            # 记录爬虫开始状态
            database.update_task_state(self.task_id, 2)
        return tasks

    def spider_exception(self, flight_date, dacode, reason, msg, errcode=-1, exc=""):
        """
        收集错误信息关闭spider
        :param flight_date:
        :param dacode:
        :param reason:
        :param msg:
        :param errcode:
        :param exc:
        :return:
        """
        self.tmp_retry_tiems = errcode
        http_proxy.retry_http_proxy(self.hp_id)
        log.error("%s %s %s %s" % (msg, flight_date, dacode, exc))
        raise CloseSpider(reason)
