#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import urllib
import requests
from lxml import etree

from scrapy.spiders import Spider
from scrapy.http.request import Request

from flightspider import database
from flightspider import settings
from flightspider.huiyou.fu.verification import verificatin_code_cookie
from flightspider.lib.tools import getdayofday
from flightspider.items import FlightSpiderDetailItem
from flightspider.lib import http_proxy


class FuDetailSpider(Spider):
    """
    福州航空运价数据
    """
    name = "fudetail"
    task_id = -1
    allowed_domains = [""]
    start_urls = ""
    tmp_retry_times = 0
    g_cookies = {}
    g_refresh_time = 0
    g_tag = True
    header = ''
    data = ''
    url = ''
    code = "FU"

    def __init__(self, task_id=None):
        if task_id:
            self.task_id = task_id
        self.http_proxy, self.hp_id = http_proxy.get_http_proxy(self.code)

    def get_tasks(self):
        """
        根据配置文件worker获取从抓取策略获取任务
        :param company:
        :return:
        """
        tasks = database.get_tasks(settings.WORKER, self.name, "FU")
        for var in tasks:
            # database.update_task_state(int(var["id"]), 1)
            database.update_task_record(int(var["id"]), "", 1)
        return tasks

    def start_requests(self):
        # 根据配置文件worker获取从抓取策略获取任务
        tasks = self.get_tasks()

        for task in tasks:
            # 记录task状态为2
            database.update_task_state(int(task["id"]), 2)

            depcode = task["depCode"]
            arrcode = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = '%s-%s' % (depcode, arrcode)
            for d in xrange(task["dateRange"]):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                if task["weeks"].find(week) < 0:
                    continue
                time.sleep(0.1)
                # print dacode, sel_date
                if not self.g_cookies:
                    self.g_cookies = verificatin_code_cookie(sel_date, depcode, arrcode)
                    self.g_refresh_time = int(time.time())
                self.header, self.data, self.url = self.get_params(sel_date, depcode, arrcode)
                yield Request(self.url, method="POST", headers=self.header, body=self.data, cookies=self.g_cookies, callback=self.parse_detail,
                              meta={'date': sel_date, 'cycle': cycle, "depcode": depcode, "arrcode": arrcode,
                                    'dacode': dacode})

    def parse_detail(self, response):
        try:
            ret = response.text
            if ret.find(u'请输入验证码') != -1:
                print "ip 被封"
                if self.g_tag and (((int(time.time())) - self.g_refresh_time) >= 60):
                    self.g_tag = False
                    print self.g_refresh_time
                    self.apply_cookie(response.meta["date"], response.meta["depcode"], response.meta["arrcode"])
                    self.g_refresh_time = int(time.time())
                    self.g_tag = True
                    self.header, self.data, self.url = self.get_params(response.meta["date"], response.meta["depcode"], response.meta["arrcode"])
                    ret = requests.post(self.url, headers=self.header, cookies=self.g_cookies, data=self.data).text
                elif self.g_tag and (((int(time.time())) - self.g_refresh_time) < 60):
                    time.sleep(3)
                    #ret = requests.post(self.url, headers=self.header, cookies=self.g_cookies, data=self.data).text
                else:
                    time.sleep(3)
                    #ret = requests.post(self.url, headers=self.header, cookies=self.g_cookies, data=self.data).text
            xml_info = etree.XML(ret)
        except:
            return

        # 过滤无航班response
        segment_num = len(xml_info.find('.//segments'))
        # 没航班
        if segment_num == 0:
            return
        items = []
        for var_flight in xrange(1, segment_num + 1):
            stop = xml_info.xpath('//segments/segment[%d]/stops' % var_flight)[0].text
            if stop != '0':
                continue
            flightno = xml_info.xpath('//segments/segment[%d]/flightno' % var_flight)[0].text
            for var_product in xrange(1, len(xml_info.find('.//products')) + 1):
                carry = xml_info.xpath('//flight/segments/segment[%d]/products/product[%d]/cabin/carrier' % (var_flight, var_product))[0].text
                if carry != u'FU':
                    share = 1
                    continue
                else:
                    share = 0
                cabinid = xml_info.xpath('//flight/segments/segment[%d]/products/product[%d]/cabin/cabinCode' % (var_flight, var_product))[0].text
                price = xml_info.xpath('//flight/segments/segment[%d]/products/product[%d]/cabin/adultFare' % (var_flight, var_product))[0].text
                surplus_ticket = xml_info.xpath('//flight/segments/segment[%d]/products/product[%d]/cabin/inventory' % (var_flight, var_product))[0].text
                item = FlightSpiderDetailItem()
                item["flightNo"] = 'FU%s' % flightno
                item["flightDate"] = response.meta["date"]
                item["cabinId"] = cabinid
                item["depCode"] = response.meta["depcode"]
                item["arrCode"] = response.meta["arrcode"]
                item["price"] = int(float(price))
                item["priceCurrency"] = 'CNY'
                item["surplusTicket"] = surplus_ticket
                item["share"] = share
                item["remarks"] = ""
                item["syncCycle"] = response.meta["cycle"]
                item["company"] = "FU"
                if item not in items:
                    items.append(item)
        return items

    def apply_cookie(self, sel_date, depcode, arrcode):
        self.g_cookies = verificatin_code_cookie(sel_date, depcode, arrcode)

    def get_params(self, sel_date, depcode, arrcode):
        url_cookie = 'http://www.fuzhou-air.cn/flight/searchflight.action?tripType=ONEWAY&orgCity1=%s' \
                     '&dstCity1=%s&flightdate1=%s&flightdate2=&adult=1&child=0&infant=0' % (depcode, arrcode,
                                                                                            sel_date)
        header = {
            "Host": "www.fuzhou-air.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/52.0.2743.116 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Referer": url_cookie,
            "Origin": "http://www.fuzhou-air.cn",
            "Content-Type": "text/plain;charset=UTF-8",
            "Connection": "keep-alive",
            "Accept": "*/*"
        }
        tmp_data = '<flight><tripType>ONEWAY</tripType><orgCity1>%s</orgCity1><dstCity1>%s</dstCity1>' \
                   '<flightdate1>%s</flightdate1>' % (depcode, arrcode, sel_date)
        data = tmp_data + '<index>1</index><times>4161146169</times><desc>coBPtm4BZy5Ly7E1arnlj9puIFHUhtk1' \
                          'qLs4qBsNS3qSK3htzLUUBjZHlu5VIIm%2B</desc></flight>'
        url = 'http://www.fuzhou-air.cn/flight/searchflight!getFlights.action'
        return header, data, url
