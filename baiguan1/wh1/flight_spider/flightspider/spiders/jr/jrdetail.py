#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson
from scrapy.http.request import Request
from flightspider.lib.tools import getdayofday
from flightspider.items import FlightSpiderDetailItem
from flightspider.spiders.base_spider import BaseSpider
from flightspider.spiders.jr.jr_fitter import fitter_jr

class JrDetailSpider(BaseSpider):
    """
    幸福航空运价数据
    """
    name = "jrdetail"
    code = "JR"
    allowed_domains = ["www.joy-air.com"]
    start_urls = "http://www.joy-air.com/pssweb/ota/flights?"

    def start_requests(self):
        tasks = self.get_tasks(self.code)
        for task in tasks:
            self.logger.debug(task)
            dst = task["depCode"]
            org = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = task["name"]
            dst_city = dacode.split('-')[0]
            arr_city = dacode.split('-')[1]
            dacode = '%s-%s' % (dst, org)
            for d in xrange(task["dateRange"]):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                url_info = self.start_urls + "adultNum=1&childNum=0&depDate=" + sel_date + "&desc=3PQ1Y2M3QVFIWTXQguWqLBLHVC7gjhJXcDarr1gyYaLVgf%232BblvpAApY8uvKXl27u3KWChaXUGk8sKFRfwDvqjh7LHrCpYZ9tP1Z4FbBDCJhZ0r7pyEPnkXc3r7sYMZQ4wLZp3B71sB7Tl9OOjmL3B%232BxwbxCyCYia9XLUgnhdmzwKMBD789Jj1Mp65XyR4oHF%232BlB9ja5gbYJCOhC4Q%232BOBbgv10LKDu%232BJDn5Yo3qp11%2FTOR%2FCN81GBCPPmebzXlgrm7g%2FK7Q%232B8czwvUrNkXvllesrs1nlitV58xIVer3RHaQeIwnKP%2FZ3XBKy8Ogib5zcmaNWpZZznpF3RfXvaqJRXHA%3D%3D&dstcity=" + arr_city \
                           + "&flightWayType=OW&orgcity=" + dst_city
                jrheader = {
                    "Accept": "application/json, text/plain, */*",
                    "Connection": "Keep-Alive",
                    "Referer": "http://www.joy-air.com/pssui/joyairportal/views/",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                                  "51.0.2704.103 Safari/537.36",
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "Accept-Language": "zh-CN,zh;q=0.8"
                }
                yield Request(url_info, method="GET", headers=jrheader, callback=self.parse_detail,
                              meta={'date': sel_date, 'cycle': cycle, "dst": dst, "org": org, 'dacode': dacode})

    def parse_detail(self, response):
        try:
            ret = response.text
            # self.logger.debug(ret)
            rst_str = simplejson.loads(ret)
            if len(rst_str["flihtProductList"]) == 0:
                return
        except Exception, e:
            self.spider_exception(response.meta["date"], response.meta["dacode"], "JR response Exception", exc=e.message)
            return
        items = []
        for index in xrange(len(rst_str["flihtProductList"])):
            flightno = rst_str["flihtProductList"][index]["goFlight"]["flightNumber"]
            # 过滤经停
            is_stop = rst_str["flihtProductList"][index]["goFlight"]["flightDetail"][0]["isStop"]
            if is_stop == True:
                continue
            for var in xrange(len(rst_str["flihtProductList"][index]["fareList"])):
                item = FlightSpiderDetailItem()
                item["company"] = "JR"
                item["flightNo"] = flightno
                item["flightDate"] = response.meta["date"]
                item["cabinId"] = rst_str["flihtProductList"][index]["fareList"][var]["fareSeglist"][0]["bookingClass"]
                self.logger.debug(response.meta)
                if response.meta["dst"] == u'SIA':
                    item["depCode"] = u'XIY'
                else:
                    item["depCode"] = response.meta["dst"]
                if response.meta["org"] == u'SIA':
                    item["arrCode"] = u'XIY'
                else:
                    item["arrCode"] = response.meta["org"]
                price = rst_str["flihtProductList"][index]["fareList"][var]["publishPrice"]
                item["priceCurrency"] = rst_str["flihtProductList"][index]["fareList"][var]["currencyCode"]
                surplus_ticket = rst_str["flihtProductList"][index]["fareList"][var]["fareSeglist"][0]["count"]
                # 进行余票格式的统一,避免直接写9造成理解成只剩9张票的错觉。
                if surplus_ticket == 9:
                    item["surplusTicket"] = '>9'
                else:
                    item["surplusTicket"] = surplus_ticket
                item["remarks"] = ''
                item["syncCycle"] = response.meta["cycle"]
                share = rst_str["flihtProductList"][index]["goFlight"]["flightDetail"][0]["isShare"]
                if not share:
                    item["share"] = 0
                else:
                    item["share"] = 1
                price_point = price.find('.')
                if price_point != -1:
                    item["price"] = price[:price_point]
                else:
                    item["price"] = price
                if item not in items:
                    items.append(item)
        items = fitter_jr(items)
        self.logger.debug(items)
        return items
