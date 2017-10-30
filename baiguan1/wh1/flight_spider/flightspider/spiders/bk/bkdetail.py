#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy import log
import urllib
import time
import simplejson

from scrapy.http.request import Request
from flightspider.huiyou.bk.bkauth import auth
from flightspider.items import FlightSpiderDetailItem
from flightspider.lib.tools import getdayofday
from flightspider.spiders.base_spider import BaseSpider
from scrapy.http.request.form import FormRequest
from flightspider.log.sentry_log import log
from scrapy.conf import settings
from flightspider import database

settings.set('DOWNLOAD_TIMEOUT',30,557)
settings.set('CONCURRENT_REQUESTS',1,558)
settings.set('RETRY_HTTP_CODES',[504],559)
settings.set('HTTPERROR_ALLOWED_CODES',[302,403,500],560)
settings.set('RETRY_ENABLED ',False,500)
settings.set('RETRY_TIMES ',0,501)
settings.set('AUTOTHROTTLE_ENABLED ',True,502)
settings.set('AUTOTHROTTLE_START_DELAY ',5,503)
settings.set('AUTOTHROTTLE_MAX_DELAY ',60,504)

class bkDetailSpider(BaseSpider):
    """
    奥凯航空航班运价数据
    """
    name = "bkdetail"
    code = "BK"
    allowed_domains = [""]
    start_urls = ""


    def start_requests(self):
        print self.http_proxy,111
        tasks = self.get_tasks(self.code)
        for task in tasks:
            depcode = task["depCode"]
            arrcode = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = '%s-%s' % (depcode, arrcode)
            # for d in xrange(task["dateRange"]):
            for d in xrange(5):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                self.logger.info('航空公司：%s日期：%s 航线：%s开始爬取数据' % (self.code, sel_date, dacode))
                # 身份认证
                try:
                    cookie, header, url = auth(self.http_proxy, depcode, arrcode, sel_date)
                except Exception as e:
                    self.logger.exception(e)
                data = {
                    'tripType': '0',
                    'orgCity': depcode,
                    'destCity': arrcode,
                    'takeoffDate': sel_date,
                    'adultNum': '1',
                    'childNum': '0'
                }
                yield FormRequest(url, method="POST", headers=header, formdata=data,
                                  callback=self.parse_detail,
                                  meta={'date': sel_date, 'cycle': cycle, 'cookies': cookie, 'task': task,
                                      'dacode': dacode,'dont_retry':True,
                                        'arrcode': arrcode, 'depcode': depcode, 'proxy': self.http_proxy})
                time.sleep(5)

    def parse_detail(self, response):
        try:
            ret = response.text
            # print ret
        except Exception, e:
            self.spider_exception(response.meta["date"], response.meta["dacode"], "BK response Exception",
                                  exc=e.message)
            return
        if response.text.find('服务器忙，请稍后再试!') != -1:
            sql = "UPDATE http_proxy SET state=%s WHERE id=%s" % (4, self.hp_id)
            database.db.update(sql)
            self.logger.warning(
                '航空公司：%s日期：%s 航线：%s' % (self.code, response.meta["date"], response.meta["dacode"] + ' ip被封'))
            self.tmp_retry_times = -1
            self.spider_exception(response.meta["date"], response.meta["dacode"], "NS response Exception",
                                  exc="NS IP blocked")
            return
        self.logger.info('航空公司：%s日期：%s 航线：%s开始处理数据' % (self.code, response.meta["date"], response.meta["dacode"]))
        """
        获取航班详细信息
        """
        items = []
        item1 = response.xpath('//div[@class="information_list"]')
        item2 = response.xpath('//div[@class="moreTicket"]')
        for i in xrange(len(item1)):
            flightNo = item1[i].xpath('.//li[1]/text()').extract()[0].strip()
            flights = []
            flights.append(item1[i].xpath('.//li')[4:9])
            flights.append(item2[i].xpath('.//li'))
            for it in flights:
                for flight in it:
                    if len(flight.xpath('text()').extract()) != 1:
                        try:
                            item = FlightSpiderDetailItem()
                            item['company'] = self.code
                            item['flightNo'] = flightNo
                            item['flightDate'] = response.meta["date"]
                            item['depCode'] = response.meta["depcode"]
                            item['arrCode'] = response.meta["arrcode"]
                            item['cabinId'] = flight.xpath('.//input/@onclick').extract()[0].split(',',5)[4].strip('"')
                            item['price'] = int(flight.xpath('.//font/text()').extract()[0].replace(',', '')[1:])
                            item['priceCurrency'] = 'CNY'
                            item['surplusTicket'] = ''  # 官网暂时没有余票数量
                            item['share'] = 0
                            item['remarks'] = ''
                            item['syncCycle'] = response.meta["cycle"]
                            items.append(item)
                        except Exception as e:
                            self.logger.info('航空公司：%s日期：%s 航线：%s错误信息：%s' % (
                            self.code, response.meta["date"], response.meta["dacode"], e))
        if not items:
            self.logger.warning(
                '航空公司：%s日期：%s 航线：%s' % (self.code, response.meta["date"], response.meta["dacode"] + '未爬取到数据'))
        self.logger.info(
            '航空公司：%s日期：%s 航线：%s爬取到的json数据%s' % (self.code, response.meta["date"], response.meta["dacode"], items))
        return items
