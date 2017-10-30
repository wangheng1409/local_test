#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy import log
import urllib
import time
import simplejson

from scrapy.http.request import Request
from flightspider.huiyou.s_9h.s_9hauth import auth
from flightspider.items import FlightSpiderDetailItem
from flightspider.lib.tools import getdayofday
from flightspider.spiders.base_spider import BaseSpider
from flightspider.log.sentry_log import log


class S_9hDetailSpider(BaseSpider):
    """
    长安航空航班运价数据
    """
    name = "s_9hdetail"
    code = "9H"
    allowed_domains = [""]
    start_urls = ""

    def start_requests(self):
        tasks = self.get_tasks(self.code)
        for task in tasks:
            depcode = task["depCode"]
            arrcode = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = '%s-%s' % (depcode, arrcode)
            for d in xrange(task["dateRange"]):
                # for d in xrange(1,7):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                self.logger.info('航空公司：%s日期：%s 航线：%s开始爬取数据' % (self.code, sel_date, dacode))
                # 身份认证
                try:
                    cookie, header, url = auth(depcode, arrcode, sel_date)
                except Exception as e:
                    self.logger.debug(e)
                yield Request(url, method="GET", headers=header, cookies=cookie,
                              callback=self.parse_detail,
                              meta={'date': sel_date, 'cycle': cycle, 'cookies': cookie, 'task': task, 'dacode': dacode,
                                    'arrcode': arrcode, 'depcode': depcode})

    def parse_detail(self, response):
        try:
            ret = response.text
        except Exception, e:
            self.spider_exception(response.meta["date"], response.meta["dacode"], "9H response Exception",
                                  exc=e.message)
            return
        if response.status == 403:
            self.logger.warning(
                '航空公司：%s日期：%s 航线：%s' % (
                    self.code, response.meta["date"], response.meta["dacode"] + '9H IP blocked'))
            self.tmp_retry_times = -1
            self.spider_exception(response.meta["date"], response.meta["dacode"], "9H response Exception",
                                  exc="9H IP blocked")

        try:
            if "警告" in response.text:
                self.logger.warning(
                    '航空公司：%s日期：%s 航线：%s 错误信息：%s' % (
                        self.code, response.meta["date"], response.meta["dacode"], '无法根据您选择的日期找到空余可用的航班，请重新选择另一个日期'))
                return
        except:
            pass
        try:
            if "错误" in response.text:
                self.logger.warning(
                    '航空公司：%s日期：%s 航线：%s 错误信息：%s' % (
                        self.code, response.meta["date"], response.meta["dacode"], "您选择的日期无航班，请重新尝试，建议选择'其它可用的旅行日期'。"))
                return
        except:
            pass
        try:
            if "系统繁忙" in response.text:
                self.logger.warning(
                    '航空公司：%s日期：%s 航线：%s 错误信息：%s' % (
                        self.code, response.meta["date"], response.meta["dacode"], "当前系统繁忙，请稍后再试"))
                return
        except:
            pass
        self.logger.info('航空公司：%s日期：%s 航线：%s开始处理数据' % (self.code, response.meta["date"], response.meta["dacode"]))
        """
        获取航班详细信息
        """
        items = []
        flights = response.xpath('//*[@id="AIR_SEARCH_RESULT_CONTEXT_ID0"]/tbody/tr/td[contains(@rowspan,"1")]')
        for flight in flights:
            try:
                item = FlightSpiderDetailItem()
                item['company'] = self.code
                item['flightNo'] = \
                    response.xpath('//*[@id="AIR_SEARCH_RESULT_CONTEXT_ID0"]/tbody/tr/td[1]/div/a/text()').extract()[0]
                item['flightDate'] = response.meta["date"]
                item['depCode'] = response.meta["depcode"]
                item['arrCode'] = response.meta["arrcode"]
                item['cabinId'] = flight.xpath('.//input/@onclick').extract()[0][26:28]
                item['price'] = int(flight.xpath('.//label/text()').extract()[0].replace(',', ''))
                item['priceCurrency'] = 'CNY'
                item['surplusTicket'] = flight.xpath('.//b/text()').extract()[0][2:3] if flight.xpath(
                    './/b/text()').extract() else '>9'
                item['share'] = 0
                item['remarks'] = ''
                item['syncCycle'] = response.meta["cycle"]
                items.append(item)
            except Exception as e:
                self.logger.info(
                    '航空公司：%s日期：%s 航线：%s错误信息：%s' % (self.code, response.meta["date"], response.meta["dacode"], e))
        if not items:
            self.logger.warning(
                '航空公司：%s日期：%s 航线：%s' % (self.code, response.meta["date"], response.meta["dacode"] + '未爬取到数据'))
        self.logger.info(
            '航空公司：%s日期：%s 航线：%s爬取到的json数据%s' % (self.code, response.meta["date"], response.meta["dacode"], items))
        return items
