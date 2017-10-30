#!/usr/bin/env python
# -*- coding: utf-8 -*-
import simplejson
import requests
import urllib

from scrapy.spiders import Spider
from scrapy.http.request import Request

from flightspider import database
from flightspider import settings
from flightspider.lib.tools import getdayofday
from flightspider.items import FlightSpiderDetailItem
from flightspider.huiyou.mf.mfauth import mf_authentication


class MfDetailSpider(Spider):
    """
    厦门航空运价数据
    """
    name = "mfdetail"
    task_id = -1
    allowed_domains = ["http://et.xiamenair.com"]
    start_urls = "http://et.xiamenair.com/xiamenair/book/findFlights.action?"
    tmp_retry_times = 0

    def start_requests(self):
        # 根据配置文件worker获取从抓取策略获取任务
        if self.task_id == -1:
            tasks = database.get_tasks(settings.WORKER, self.name, "MF")
        else:
            tasks = database.get_tasks("", "", "", self.task_id)
            # 记录爬虫开始状态
            database.update_task_state(self.task_id, 2)

        for task in tasks:
            depcode = task["depCode"]
            arrcode = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = task["name"]
            for d in xrange(task["dateRange"]):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                mf_cookie, r, time_info = mf_authentication(depcode, arrcode, sel_date)
                # 请求航班信息
                mf_first_header = {
                    "Host": "et.xiamenair.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
                    "Accept": "*/*",
                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": "http://et.xiamenair.com/xiamenair/book/findFlights.action?tripType=0&"
                               "queryFlightInfo=%s,%s,%s&cabinClass=1&psgrInfo=0,1;1,0" % (depcode, arrcode, sel_date),
                    "Connection": "keep-alive"
                }
                cookies = {
                    "JSESSIONID": mf_cookie["JSESSIONID"],
                    "Webtrends": mf_cookie["Webtrends"],
                    "BIGipServerpool_122.119.114.103": mf_cookie["BIGipServerpool_122.119.114.103"],
                    "WT_FPC=id": mf_cookie["WT_FPC"]
                }

                params = {
                    "r": r,
                    "lang": "zh",
                    "takeoffDate": "%s" % sel_date,
                    "returnDate": "",
                    "orgCity": "%s" % depcode,
                    "dstCity": "%s" % arrcode,
                    "tripType": 0,
                    "_": time_info
                }
                url_params = urllib.urlencode(params)
                url = r'http://et.xiamenair.com/xiamenair/book/findFlights.json?' + url_params
                yield Request(url, method="GET", headers=mf_first_header, cookies=cookies, callback=self.parse_detail,
                              meta={'date': sel_date, 'cycle': cycle, "depcode": depcode, "arrcode": arrcode, 
                                    'dacode': dacode, 'r': r, 'mf_cookie': mf_cookie})


    def parse_detail(self, response):
        try:
            ret = response.text
        except:
            return

        try:
            json_info = simplejson.loads(ret)
        except Exception, e:
            return
        if json_info["resultCode"] != '00':
            return
        # 初始页面显示信息的name
        lists = ["cBrand", "fBrand", "iBrand", "yBrand"]
        takeoffDate = json_info["takeoffDate"]
        tripType = json_info["tripType"]

        items = []
        for linear in json_info["flightInfos1"]:
            bottomCabin = ""
            for item_part in lists:
                # 航班信息状态:1为正常,2为不可买票,3为航班已经起飞
                if linear["state"] != 1:
                    continue
                item = FlightSpiderDetailItem()
                # 过滤经停
                stop = linear["stop"]
                if stop:
                    continue

                item["flightDate"] = response.meta["date"]
                #item["daCode"] = response.meta["dacode"]
                item["depCode"] = response.meta["depcode"]
                item["arrCode"] = response.meta["arrcode"]
                depcode = linear["org"]
                arrcode = linear["dst"]
                item["company"] = linear["airline"]
                if linear["codeShare"] == False:
                    share = 0
                else:
                    share = 1
                    return
                item["share"] = share
                item["priceCurrency"] = "CNY"
                item["syncCycle"] = response.meta["cycle"]
                item["remarks"] = ""
                # 第一次查询的parse
                if linear[item_part] is None:
                    continue
                item["cabinId"] = linear[item_part]["cabin"]
                if item_part == "cBrand":
                    bottomCabin = item["cabinId"]
                item["flightNo"] = "MF%s" % linear[item_part]["fltNO"]
                item["surplusTicket"] = linear[item_part]["seats"]
                item["price"] = linear[item_part]["price"]
                if item not in items:
                    items.append(item)
            if bottomCabin:
                items = self.detail_request(items, json_info, linear, takeoffDate, tripType, response, bottomCabin)
        return items

    def detail_request(self, items, json_info, linear, takeoffDate, tripType, response, bottomCabin):
        cookie = response.meta["mf_cookie"]
        r = response.meta["r"]
        # 请求航班详细信息
        json_post = {"org": json_info["orgCity"],
                     "dst": json_info["dstCity"],
                     "takeoffDate": takeoffDate,
                     "returnDate": None,
                     "takeoffTime": linear["takeoffTime"],
                     "arrivalTime": linear["arrivalTime"],
                     "tripType": tripType,
                     "stop": linear["stop"],
                     "equipment": linear["equipment"],
                     "fltNo": linear["fltNo"],
                     "airline": linear["airline"],
                     "arriveAd": None,
                     "classes": linear["classes"],
                     "codeShareList": None,
                     "curTrip": 0,
                     "bottomCabin": bottomCabin#linear["cBrand"]["cabin"]
                     }
        header_more = {
            "Host": "et.xiamenair.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://et.xiamenair.com/xiamenair/book/findFlights.action?tripType=0"
                       "&queryFlightInfo=%s,%s,%s&cabinClass=1&psgrInfo=0,1;1,0" % (json_info["orgCity"],
                                                                                    json_info["dstCity"], takeoffDate),
            "Cookie": "JSESSIONID=" + cookie["JSESSIONID"] + "; " +
                      "Webtrends=" + cookie["Webtrends"] + "; " +
                      "BIGipServerpool_122.119.114.103=" + cookie["BIGipServerpool_122.119.114.103"] +
                      "; WT_FPC=id=" + cookie["WT_FPC"] + "; _pk_ref.1.7ca2=" + cookie["_pk_ref.1.7ca2"] +
                      "; _pk_id.1.7ca2=" + cookie["_pk_id.1.7ca2"] + "; _pk_ses.1.7ca2=" + cookie["_pk_ses.1.7ca2"],
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        }
        url_more = 'http://et.xiamenair.com/xiamenair/book/findMore.json?r=%s&org=%s&dst=%s&date=%s' \
                   '&tripType=0&curTrip=0&fltNo=MF%s&update=aq20150421' % \
                   (r, json_info["orgCity"], json_info["dstCity"], takeoffDate, linear["fltNo"])
        more_info = requests.post(url_more, headers=header_more, json=json_post).text
        more_json = simplejson.loads(more_info)
        if more_json["resultCode"] != '00':
            return items

        for var in more_json["brandList"]:
            item = FlightSpiderDetailItem()
            item["flightNo"] = "MF%s" % var["fltNO"]
            item["flightDate"] = takeoffDate
            item["cabinId"] = var["cabin"]
            #item["daCode"] = response.meta["dacode"]
            item["depCode"] = response.meta["depcode"]
            item["arrCode"] = response.meta["arrcode"]
            item["price"] = var["price"]
            item["priceCurrency"] = "CNY"
            item["surplusTicket"] = var["seats"]
            item["share"] = 0
            item["company"] = "MF"
            item["remarks"] = ""
            item["syncCycle"] = response.meta["cycle"]
            if item not in items:
                items.append(item)
        return items



