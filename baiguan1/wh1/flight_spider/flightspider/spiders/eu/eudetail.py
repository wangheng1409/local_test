#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flightspider.lib.tools import getdayofday
from scrapy.http.request.form import FormRequest
from flightspider.items import FlightSpiderDetailItem
from flightspider.spiders.base_spider import BaseSpider


class EuDetailSpider(BaseSpider):
    """
    成都航空运价数据
    """
    name = "eudetail"
    code = "EU"
    allowed_domains = ["http://b2c.chengduair.cc"]
    start_urls = "http://b2c.chengduair.cc/euair/reservation/flightQuery.do"

    def start_requests(self):
        tasks = self.get_tasks(self.code)
        for task in tasks:
            depcode = task["depCode"]
            arrcode = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = task["name"]
            # 获取cookie
            url = 'http://b2c.chengduair.cc/euair/index.jsp'
            session = requests.session()
            rtn = session.get(url)
            dict_cookies = requests.utils.dict_from_cookiejar(session.cookies)

            for d in xrange(task["dateRange"]):
            # for d in xrange(28,29):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                if task["weeks"].find(week) < 0:
                    continue

                euheader = {
                    "Host": "b2c.cdal.com.cn",
                    "Connection": "keep-alive",
                    "Content - Length": "122",
                    "Cache - Control": "max - age = 0",
                    "Origin": "http: // b2c.cdal.com.cn",
                    "Upgrade - Insecure - Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Referer":"http://b2c.cdal.com.cn/euair/reservation/flightQuery.do" ,
                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate",
                    "Cookie": dict_cookies

                }
                url_info = "http://b2c.chengduair.cc/euair/reservation/flightQuery.do"

                data = {
                    "orgCity": "%s" % depcode,
                    "takeoffDate": "%s" % sel_date,
                    "returnDate": "%s" % sel_date,
                    "tripType": "0",
                    "destCity": "%s" % arrcode,
                    "adultNum": "1",
                    "childNum": "0",
                    "babyNum": "0",
                    'x':'32',
                    'y':'12'
                }
                self.logger.info('航空公司：%s 日期：%s  航线：%s开始爬取数据' % (self.code, sel_date, dacode))
                yield FormRequest(url_info, headers=euheader, formdata=data, callback=self.parse_detail,
                                  meta={'date': sel_date, 'cycle': cycle, "depcode": depcode, "arrcode": arrcode, 'dacode': dacode})



    def parse_detail(self, response):

        try:
            ret = response.text
        except Exception, e:
            self.spider_exception(response.meta["date"], response.meta["dacode"], "EU response Exception", exc=e.message)
            return
        self.logger.info('航空公司：%s 日期：%s 航线：%s开始处理数据' % (self.code, response.meta["date"], response.meta["dacode"]))
        items = []
        item1=response.xpath('//tr[@class="air_line"]')
        item2=response.xpath('//tr[@class="air_line show_more_tr"]')
        for i in xrange(len(item1)):
            flightNo=item1[i].xpath('.//td[2]/text()').extract()[0].strip()
            flights=[]
            flights.append(item1[i].xpath('.//td')[5:-1])
            flights.append(item2[i].xpath('.//p'))

            for item in flights:
                for flight in item:
                    if len(flight.xpath('text()').extract())!=1:
                        try:
                            item = FlightSpiderDetailItem()
                            item['company'] = self.code
                            item['flightNo'] = flightNo
                            item['flightDate'] = response.meta["date"]
                            item['depCode'] = response.meta["depcode"]
                            item['arrCode'] = response.meta["arrcode"]
                            item['cabinId'] = flight.xpath('.//span[1]/text()').extract()[0][0]
                            item['price'] = int(flight.xpath('text()').extract()[2].strip()[1:] or flight.xpath('text()').extract()[3].strip()[1:])
                            item['priceCurrency'] = 'CNY'
                            item['surplusTicket'] = flight.xpath('.//span[2]/text()').extract()[0]
                            item['share'] = 0
                            item['remarks'] = ''
                            item['syncCycle'] = response.meta["cycle"]
                            items.append(item)
                        except Exception as e:
                            self.logger.info(
                                '航空公司：%s 日期：%s 航线：%s 错误信息：%s' % (self.code, response.meta["date"], response.meta["dacode"], e))
        if not items:
            self.logger.warning(
                '航空公司：%s 日期：%s 航线：%s' % (self.code, response.meta["date"], response.meta["dacode"] + '未爬取到数据'))
        self.logger.info(
            '航空公司：%s 日期：%s 航线：%s爬取到的json数据%s' % (self.code, response.meta["date"], response.meta["dacode"], items))
        return items
