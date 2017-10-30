#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import json
from flightspider import database
from scrapy.http.request.form import FormRequest
from flightspider.lib.tools import getdayofday
from flightspider.items import FlightSpiderDetailItem
from flightspider.spiders.base_spider import BaseSpider
from flightspider.huiyou.ns.auth import ns_authentication
import requests

from scrapy.conf import settings
from flightspider import settings as se
settings.set('DOWNLOAD_TIMEOUT', 30, 557)
settings.set('CONCURRENT_REQUESTS', 20, 558)
settings.set('RETRY_HTTP_CODES', [504], 559)
settings.set('HTTPERROR_ALLOWED_CODES', [302,403,500], 560)
settings.set('RETRY_ENABLED ', False, 499)
settings.set('RETRY_TIMES ', 0, 501)



class NsDetailSpider(BaseSpider):
    """
    河北航空运价数据
    """
    name = "nsdetail"
    code = "NS"
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
            #for d in xrange(1, 2):
                if d%2==0:
                    index=d/2
                else:
                    index=(d-1)/2

                try:
                    self.http_proxy =se.PROXY_LIST[int(self.ipindex)][index]
                except:
                    self.http_proxy = ''

                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                self.logger.info('航空公司：%s日期：%s 航线：%s开始爬取数据' % (self.code, sel_date, dacode))
                # 身份认证
                try:
                    cookie, header, url = ns_authentication(self.http_proxy,depcode, arrcode, sel_date)
                except requests.ConnectionError as e:
                    sql = "UPDATE http_proxy SET state=%s WHERE id=%s" % (3, self.hp_id)
                    database.db.update(sql)
                    self.logger.warning(
                        '航空公司：%s日期：%s 航线：%s' % (self.code, sel_date, dacode + 'ip被封'))
                    self.tmp_retry_times = -1
                    self.spider_exception(sel_date, dacode, "NS response Exception",
                                          exc="NS IP blocked")
                    return
                except Exception as e:
                    self.logger.exception(e)
                data = {
                    'dept': depcode,
                    'arri': arrcode,
                    'd1': sel_date
                }
                yield FormRequest(url, method="GET", headers=header, formdata=data, cookies=cookie,
                                  callback=self.parse_detail,
                                  meta={'date': sel_date, 'cycle': cycle, 'cookies': cookie, 'task': task,
                                        'dacode': dacode, # 'dont_retry':True,
                                        'arrcode': arrcode, 'depcode': depcode, 'proxy': self.http_proxy})


    def parse_detail(self, response):

        """
          获取航班详细信息
          """
        if response.status == 500:
            self.logger.warning(
                '航空公司：%s日期：%s 航线：%s' % (self.code, response.meta["date"], response.meta["dacode"] + response.text))
            return

        if response.status == 403 or response.text.find('服务器忙，请稍后再试!') != -1:
            sql = "UPDATE http_proxy SET state=%s WHERE id=%s" % (3, self.hp_id)
            database.db.update(sql)
            self.logger.warning(
                '航空公司：%s日期：%s 航线：%s' % (self.code, response.meta["date"], response.meta["dacode"] + 'ip被封'))
            self.tmp_retry_times = -1
            self.spider_exception(response.meta["date"], response.meta["dacode"], "NS response Exception",
                                  exc="NS IP blocked")
            return
        try:
            ret = json.loads(response.text)
        except Exception, e:
            self.spider_exception(response.meta["date"], response.meta["dacode"], "NS response Exception",
                                  exc=e.message)
            return

        self.logger.info('航空公司：%s日期：%s 航线：%s开始处理数据' % (self.code, response.meta["date"], response.meta["dacode"]))

        items = []
        flights = ret['d1']['flights']
        flightDate = response.meta["date"]
        depCode = response.meta["depcode"]
        arrCode = response.meta["arrcode"]
        syncCycle = response.meta["cycle"]

        # from json data get cabin_list
        try:
            for it in flights:
                for directflight in it['directFlight']:
                    flightNo = directflight['flightNo']
                    shareFlight = directflight['shareFlight']
                    cabin_list = []
                    for product in directflight['products']:
                        for cabins_category in product['cabins']:
                            cabin_list.append(cabins_category)

                    item = self.deal_cabin(flightNo, shareFlight, cabin_list, flightDate, depCode, arrCode, syncCycle)
                    items.extend(item)
        except Exception as e:
            self.logger.warning(
                '航空公司：%s日期：%s 航线：%s 错误信息%s' % (self.code, response.meta["date"], response.meta["dacode"], e))

        if not items:
            self.logger.warning(
                '航空公司：%s日期：%s 航线：%s' % (self.code, response.meta["date"], response.meta["dacode"] + '未爬取到数据'))
        self.logger.info(
            '航空公司：%s日期：%s 航线：%s爬取到的json数据%s' % (self.code, response.meta["date"], response.meta["dacode"], len(items)))
        return items

    def deal_cabin(self, flightNo, shareFlight, cabin_list, flightDate, depCode, arrCode, syncCycle):
        '''
            formart cabin_list to items
        :param flightNo:
        :param shareFlight: 是否共享航班
        :param cabin_list:
        :param flightDate:
        :param depCode:
        :param arrCode:
        :param syncCycle:
        :return:
        '''
        items = []
        for cabin in cabin_list:
            item = FlightSpiderDetailItem()
            item['company'] = self.code
            item['flightNo'] = flightNo
            item['flightDate'] = flightDate
            item['depCode'] = depCode
            item['arrCode'] = arrCode
            item['cabinId'] = cabin['name']
            item['price'] = int(cabin['price'])
            item['priceCurrency'] = 'CNY'
            item['surplusTicket'] = '>9' if cabin['seatNum'] == 'A' else cabin['seatNum']
            item['share'] = shareFlight if shareFlight else 0
            item['remarks'] = ''
            item['syncCycle'] = syncCycle
            items.append(item)
        return items
