#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

import uuid
import time
import urllib
import random
import simplejson

from scrapy.http.request import Request

from flightspider import settings
from flightspider.huiyou.ca.caauth import ca_authentication
from flightspider.items import FlightSpiderDetailItem
from flightspider.lib.tools import getdayofday, url_qs
from flightspider.lib import test_modify_router
from flightspider.log.sentry_log import log
from flightspider.spiders.base_spider import BaseSpider


class CaDetailSpider(BaseSpider):
    """
    中国国航航班运价数据
    """
    name = "cadetail"
    code = "CA"
    allowed_domains = ["airchina.com.cn"]
    start_urls = "https://m.airchina.com.cn:9061/worklight/apps/services/api/AirChina/android/query"
    handle_httpstatus_list = [401, 403]

    def start_requests(self):
        tasks = self.get_tasks(self.code)
        for task in tasks:
            dst = task["depCode"]
            org = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = task["name"]
            try:
                # 身份认证
                ca = ca_authentication(self.start_urls, self.http_proxy)
                # 请求列表 组合请求参数
                log.debug(ca)
                headers = ca[0]
                cookies = ca[1]
                params = ca[2]
                headers.pop("Authorization")
            except Exception, e:
                log.error("auth %s,%s:%s" % (dst, org, e))
                continue
            for d in xrange(task["dateRange"]):
                time.sleep(settings.DOWNLOAD_DELAY)
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                log.debug("%s==>%s==%s" % (dst, org, sel_date))
                if task["weeks"].find(week) < 0:
                    continue

                # 请求列表 组合请求参数
                params["procedure"] = "qryFlights"
                params["adapter"] = "ACFlight"
                params["x"] = "%s68378" % str(random.random())[0:13]
                time_stamp = "%d236" % int(time.time())
                cabin = "Economy"
                backDate = ""
                req_str = "[{\"req\":\"{\\\"adt\\\":\\\"1\\\",\\\"timestamp\\\":\\\"" + time_stamp + "\\\",\\\"backDate\\\":\\\"" \
                          + backDate + "\\\",\\\"org\\\":\\\"" + org + "\\\",\\\"dst\\\":\\\"" + dst \
                          + "\\\",\\\"token\\\":\\\"11111111\\\",\\\"version\\\":\\\"1\\\",\\\"date\\\":\\\"" \
                          + sel_date + "\\\",\\\"cabin\\\":\\\"" + cabin + "\\\",\\\"flag\\\":\\\"0\\\",\\\"inf\\\":\\\"0\\\"," \
                                                                           "\\\"cnn\\\":\\\"0\\\"}\",\"lang\":\"zh_CN\",\"token\":\"11111111\"}]"
                params["parameters"] = req_str
                yield Request(self.start_urls, method="POST", body=urllib.urlencode(params), headers=headers,
                              cookies=cookies, callback=self.parse, meta={'date': sel_date, 'cycle': cycle, 'cookies': cookies,
                                                                          'dst': dst, 'org': org, "proxy": self.http_proxy,
                                                                          'dacode': dacode})

    def parse(self, response):
        """
        获取航班列表
        """
        if response.status in self.handle_httpstatus_list:
            test_modify_router.dial()
        try:
            rst = simplejson.loads(response.body[11:][:-2])
        except:
            rst = simplejson.loads(response.body)

        if not rst.get("isSuccessful", False):
            log.error("fight list: %s, %s=>%s==%s" % (response.body, response.meta["dst"], response.meta["org"], response.meta["date"]))
        for flight in rst["resp"]["goto"]["flightInfomationList"]:
            fsl = flight["flightSegmentList"][0]
            if fsl["operatingAirline"] == "CA":
                takeoffdate = fsl["flightDepdatePlan"] + "T" + fsl["flightDeptimePlan"][:8]
                arrivedate = fsl["flightArrdatePlan"] + "T" + fsl["flightArrtimePlan"][:8]
                req_str = '[{\"token\":\"11111111\",\"req\":"{\\\"takeoffdate\\\":\\\"' + takeoffdate \
                          + '\\\",\\\"childNum\\\":\\\"0\\\",\\\"adultNum\\\":\\\"1\\\",\\\"flag\\\":\\\"0\\\",\\\"dst\\\":\\\"' \
                          + fsl["flightDep"] + '\\\",\\\"org\\\":\\\"' + fsl["flightArr"] + '\\\",\\\"flightID\\\":\\\"' + flight["flightID"] \
                          + '\\\",\\\"flightno\\\":\\\"' + fsl["flightNo"][-4:] + '\\\",\\\"searchId\\\":\\\"' + fsl["searchId"] \
                          + '\\\",\\\"infantNum\\\":\\\"0\\\",\\\"airline\\\":\\\"' + fsl["operatingAirline"] + '\\\",\\\"arrivedate\\\":\\\"' \
                          + arrivedate + '\\\"}\",\"lang\":\"zh_CN\"}]'
                headers = response.request.headers
                headers["x-wl-analytics-tracking-id"] = str(uuid.uuid1())
                params = url_qs(urllib.unquote(response.request.body))
                log.debug(str(params))
                params["procedure"] = "qryFlightDetail"
                params["adapter"] = "ACFlight"
                params["x"] = "%s6837" % random.random()
                params["parameters"] = req_str
                response.meta["flight_no"] = fsl["flightNo"]
                yield Request(response.url, method="POST", body=urllib.urlencode(params), headers=headers, cookies=response.meta["cookies"],
                              callback=self.parse_detail, meta=response.meta)

    def parse_detail(self, response):
        """
        获取航班详细信息
        """
        # try:
        if response.status in self.handle_httpstatus_list:
            test_modify_router.dial()
        try:
            rst = simplejson.loads(response.body[11:][:-2])
        except:
            rst = simplejson.loads(response.body)

        if rst.get("isSuccessful") and rst["resp"]["code"] == "00000000":
            log.debug("%s==>%s==%s==%s" % (response.meta["dst"], response.meta["org"], response.meta["date"], response.body))
            items = []
            for flight in rst["resp"]["FFCabins"]:
                item = FlightSpiderDetailItem()
                item["flightNo"] = response.meta["flight_no"]
                item["flightDate"] = response.meta["date"]
                item["cabinId"] = flight.get("ffcabinId")
                item["daCode"] = response.meta["dacode"]
                item["price"] = int(flight.get("price"))
                item["priceCurrency"] = flight.get("priceCurrency")
                item["surplusTicket"] = "A"
                if flight.get("surplusTicket", ""):
                    item["surplusTicket"] = flight.get("surplusTicket")
                # item["surplusTicket"] = flight.get("surplusTicket")
                item["share"] = 0
                if flight["isShared"] == "0":
                    item["share"] = 1
                item["remarks"] = simplejson.dumps(flight)
                item["syncCycle"] = response.meta["cycle"]
                items.append(item)
            return items
        else:
            log.error("%s==>%s==%s==%s" % (response.meta["dst"], response.meta["org"], response.meta["date"], response.body))
        # except Exception, e:
        #     log.error("fight detail: %s\n:%s %s=>%s==%s" % (e, response.body, response.meta["dst"], response.meta["org"], response.meta["date"]))
