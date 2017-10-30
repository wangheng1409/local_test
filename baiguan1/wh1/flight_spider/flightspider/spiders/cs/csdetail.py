#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

import time
import urllib
import simplejson

from scrapy.http.request import Request
from flightspider.huiyou.cs.csauth import cs_authentication
from flightspider.items import FlightSpiderDetailItem
from flightspider.lib.tools import getdayofday
from flightspider.huiyou.cs import southair_dec_data
from flightspider.spiders.base_spider import BaseSpider
from flightspider.log.sentry_log import log


MSG_01 = u"暂时没有符合条件的航班，请换个日期或航线试试【IS0004】" # 没有票
MSG_02 = u"暂时没有符合条件的航班，请换个日期或航线试试【ZS0004】" # 没有开通航班


class CsDetailSpider(BaseSpider):
    """
    中国南方航班运价数据
    """
    name = "csdetail"
    code = "CZ"
    allowed_domains = ["3g.csair.com"]
    start_urls = "http://3g.csair.com/CSMBP/data/order/getAvPriceForJson.do?"
    handle_httpstatus_list = [401, 403]

    def start_requests(self):
        tasks = self.get_tasks(self.code)
        for task in tasks:
            dst = task["depCode"]
            org = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = task["name"]
            # 身份认证
            try:
                cs = cs_authentication(self.http_proxy)
            except Exception, e:
                exc = "%r:%r" % (Exception, e)
                self.spider_exception("0000-00-00", dacode, "CS Authentioincation Exception",
                                      "request cs authentication",
                                      exc=exc)
            for d in xrange(task["dateRange"]):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                sel_date = sel_date.replace("-", "")
                if task["weeks"].find(week) < 0:
                    continue

                # 请求列表 组合请求参数
                headers = cs[0]
                cookies = cs[1]
                params = cs[2]
                url = self.start_urls + urllib.urlencode(params)
                params["timestamp"] = "%d236" % int(time.time())
                params = southair_dec_data.enc_req_data('{"CHILDNUM":"0","CITIES":[{"ARRCITY":"' + org + '","DEPCITY":"'
                              + dst + '"}],"ADULTNUM":"1","SEGTYPE":"S","ISLOGIN":false,"DATES":["' + sel_date + '"]}')
                yield Request(url, method="POST", body=params, headers=headers, cookies=cookies,
                              callback=self.parse_detail, meta={'date': sel_date, 'cycle': cycle,
                                                                'proxy': self.http_proxy, 'dacode': dacode})

    def parse_detail(self, response):
        """
        获取航班详细信息
        """
        flight_date = response.meta["date"]
        dacode = response.meta["dacode"]
        rst = southair_dec_data.dec_resp_data(response.body)
        try:
            rst_str = simplejson.loads(rst)
            if rst_str.get("session") and rst_str["session"]["channel"] == "MOBILE":
                items = []
                for flights in rst_str["FLIGHTS"]["SEGMENT"][0]["DATEFLIGHT"]:
                    for cabin in flights["CABINS"]:
                        item = FlightSpiderDetailItem()
                        item["flightNo"] = flights["FLIGHTNO"]
                        item["flightDate"] = flight_date
                        item["cabinId"] = cabin.get("NAME")
                        item["daCode"] = dacode
                        item["price"] = int(cabin.get("CHILDPRICE"))
                        item["priceCurrency"] = "CNY"
                        # item["surplusTicket"] = -1
                        # if cabin.get("INFO") != ">9":
                        #     item["surplusTicket"] = int(cabin.get("INFO"))
                        item["surplusTicket"] = cabin.get("INFO")
                        item["share"] = 0
                        if flights["CODESHARE"] == "TRUE":
                            item["share"] = 1
                        item["remarks"] = simplejson.dumps(cabin)
                        item["syncCycle"] = response.meta["cycle"]
                        items.append(item)
                return items
            else:
                msg = "%s:%s:%s" % (flight_date, dacode, rst)
                log.info(msg)
        except Exception, e:
            sel_date = getdayofday()
            sel_date = sel_date.replace("-", "")
            if sel_date != flight_date:
                exc = "%r:%r:%s" % (Exception, e, rst)
                self.spider_exception(flight_date, dacode, "IP Exception", "request CS flight detail error", exc=exc)


