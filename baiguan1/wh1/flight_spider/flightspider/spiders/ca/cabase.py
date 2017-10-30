#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

import urllib
import time
import random
import simplejson

from scrapy import log
from scrapy.spiders import Spider
from scrapy.http.request import Request
from flightspider.items import FlightSpiderBaseItem
from flightspider.huiyou.ca.caauth import ca_authentication


class CaBaseSpider(Spider):
    """
    中国国航航班基础数据
    """
    name = "cabase"
    allowed_domains = ["airchina.com.cn"]

    handle_httpstatus_list = [401]

    start_urls = "https://m.airchina.com.cn:9061/worklight/apps/services/api/AirChina/android/query"

    def __init__(self, condition):
        if not condition:
            log.logger.debug("param error")
        param = condition.split(";")
        self.sel_date = param[0]
        self.org = param[1]
        self.dst = param[2]
        self.season = param[3]
        # 请求认证
        ca = ca_authentication(self.start_urls)
        if not ca:
            log.logger.error("ca authentication fail")

        self.headers = ca[0]
        self.cookies = ca[1]
        self.params = ca[2]

        # 组合请求参数
        self.params["procedure"] = "qryFlights"
        self.params["adapter"] = "ACFlight"
        self.params["x"] = "%s6837" % random.random()
        time_stamp = "%d236" % int(time.time())
        cabin = "Economy"
        req_str = "[{\"req\":\"{\\\"adt\\\":\\\"1\\\",\\\"timestamp\\\":\\\"" + time_stamp + "\\\",\\\"backDate\\\":\\\"\\\",\\\"org\\\":\\\"" + self.org + "\\\",\\\"dst\\\":\\\"" + self.dst \
                  + "\\\",\\\"token\\\":\\\"11111111\\\",\\\"version\\\":\\\"1\\\",\\\"date\\\":\\\"" \
                  + self.sel_date + "\\\",\\\"cabin\\\":\\\"" + cabin + "\\\",\\\"flag\\\":\\\"0\\\",\\\"inf\\\":\\\"0\\\"," \
                                                                        "\\\"cnn\\\":\\\"0\\\"}\",\"lang\":\"zh_CN\",\"token\":\"11111111\"}]"
        self.params["parameters"] = req_str

    def start_requests(self):
        yield Request(self.start_urls, method="POST", body=urllib.urlencode(self.params), headers=self.headers,
                      cookies=self.cookies)

    def parse(self, response):
        rst = simplejson.loads(response.body[11:][:-2])
        if not rst.get("isSuccessful", False):
            log.logger.debug(response.body)
        items = []
        for flight in rst["resp"]["goto"]["flightInfomationList"]:
            item = FlightSpiderBaseItem()
            fsl = flight["flightSegmentList"][0]
            if fsl["operatingAirline"] == "CA":
                item['flightNo'] = fsl["flightNo"]
                item['depcode'] = self.org
                item['arrcode'] = self.dst
                item['company'] = fsl["operatingAirline"]
                item['season'] = int(self.season)
                item['depPlanTime'] = fsl["flightDeptimePlan"][:8]
                item['arrPlanTime'] = fsl["flightArrtimePlan"][:8]
                items.append(item)
        return items
