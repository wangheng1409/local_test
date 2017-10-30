#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import time
import simplejson

from scrapy.http.request import Request
from flightspider.huiyou.a6.a6auth import auth
from flightspider.items import FlightSpiderDetailItem
from flightspider.lib.tools import getdayofday
from flightspider.spiders.base_spider import BaseSpider
from flightspider.log.sentry_log import log


class A6DetailSpider(BaseSpider):
    """
    云南红土航空航班运价数据
    """
    name = "a6detail"
    code = "A6"
    allowed_domains = [""]
    start_urls = ""

    def start_requests(self):
        print 111
        tasks = self.get_tasks(self.code)
        for task in tasks:
            depcode = task["depCode"]
            arrcode = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = '%s-%s' % (depcode, arrcode)
            for d in xrange(task["dateRange"]):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)

                # 身份认证
                cookie, header, url = auth(depcode, arrcode, sel_date)
                yield Request(url, method="GET", headers=header, cookies=cookie,
                              callback=self.parse_detail, meta={'date': sel_date, 'cycle': cycle, 'depcode': depcode,
                                                                'arrcode': arrcode, 'dacode': dacode})


    def parse_detail(self, response):
        print 'parse_detail start',response
        """
        获取航班详细信息
        """
        try:
            rst_str = simplejson.loads(response.text)
            rst_str["flights"][0]["segments"][0]
        except:
            return
        items = []
        for item in rst_str["flights"]:
            stop_city = ""
            try:
                stop_city = item["segments"][0]["avFlightShopping"]["stopCity"]
            except:
                pass
            if stop_city != "":
                break
            for var in item["segments"][0]["cabinPrices"]:
                flightno = var["airline"]
                cabin = var["cabin"]
                price = var["price"]

                item = FlightSpiderDetailItem()
                item["company"] = "A6"
                item["flightNo"] = flightno
                item["flightDate"] = response.meta["date"]
                item["cabinId"] = cabin
                item["depCode"] = response.meta["depcode"]
                item["arrCode"] = response.meta["arrcode"]
                item["price"] = price
                item["priceCurrency"] = "CNY"
                item["surplusTicket"] = "A"
                if flightno[:2] != 'A6':
                    item["share"] = 1
                else:
                    item["share"] = 0
                item["remarks"] = ""
                item["syncCycle"] = response.meta["cycle"]
                items.append(item)
        print items,'items'
        return items
