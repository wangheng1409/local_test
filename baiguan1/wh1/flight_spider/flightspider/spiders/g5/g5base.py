#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib

from lxml import etree

from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.exceptions import CloseSpider

from flightspider import database
from flightspider import settings
from flightspider.lib.tools import getdayofday
from flightspider.lib import http_proxy
from flightspider.items import FlightSpiderBaseItem


class G5BaseDetailSpider(Spider):
    name = "g5base"
    task_id = -1
    allowed_domains = ["http://www.chinaexpressair.com"]
    start_urls = "http://www.chinaexpressair.com/flight.ac?"
    http_proxy = ""
    hp_id = -1
    tmp_retry_times = 0

    def __init__(self, task_id=None):
        if task_id:
            self.task_id = task_id
        self.http_proxy, self.hp_id = http_proxy.get_http_proxy("chinaexpressair")

    def start_requests(self):
        # 根据配置文件worker获取从抓取策略获取任务
        if self.task_id == -1:
            tasks = database.get_tasks(settings.WORKER, self.name, "G5")
        else:
            tasks = database.get_tasks("", "", "", self.task_id)
            # 记录爬虫开始状态
            database.update_task_state(self.task_id, 2)

        for task in tasks:
            dst = task["depCode"]
            org = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = '%s-%s' % (dst, org)
            dst_city, org_city = task["name"].split('-')

            url_jsessionid = 'http://www.chinaexpressair.com/'
            # 重试次数
            retry_num = 1
            session = requests.session()

            while 1:
                session.proxies = {
                    'http': self.http_proxy
                }
                try:
                    res = session.get(url_jsessionid, timeout=10)
                    res_cookie = requests.utils.dict_from_cookiejar(res.cookies)
                    if res_cookie["JSESSIONID"]:
                        break
                except:
                    if retry_num == 2:
                        http_proxy.retry_http_proxy(self.hp_id)
                        self.http_proxy, self.hp_id = http_proxy.get_http_proxy(self.allowed_domains[0])
                    elif retry_num == 3:
                        self.spider_exception("IP Exception", "request CS flight detail error", errcode=-1)
                        return
                    retry_num += 1
            print res_cookie["JSESSIONID"]
            for d in xrange(task["dateRange"]):
                sel_date, week = getdayofday(d, True)

                g5header = {
                    "Host": "www.chinaexpressair.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
                    "Accept": "text/html, */*; q=0.01",
                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": "http://www.chinaexpressair.com/flight.ac?reqCode=queryFlights",
                    "Cookie": "JSESSIONID=" + res_cookie["JSESSIONID"],
                    "Connection": "keep-alive"
                }
                # 反爬虫机制的header
                g5header_spider = {
                    "Host": "www.chinaexpressair.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
                    "Accept": "*/*",
                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate",
                    "Referer": "http://www.chinaexpressair.com/index.html",
                    "Cookie": "JSESSIONID=" + res_cookie["JSESSIONID"],
                    "Connection": "keep-alive"
                }
                url_spider = 'http://www.chinaexpressair.com/webpage/webcms/js/blackip.js'
                requests.get(url_spider, headers=g5header_spider)

                data = {
                    "getcity_name": "%s" % org_city.encode('utf-8'),
                    "homecity_name": "%s" % dst_city.encode('utf-8'),
                    "sdate": "%s" % sel_date.encode('utf-8'),
                    "adult": 1,
                    "child": 0,
                    "baby": 0,
                    "flag": 1
                }
                params = urllib.urlencode(data)
                url_info = 'http://www.chinaexpressair.com/flight.ac?reqCode=queryAjaxFlights'
                yield Request(url_info, method="POST", body=params, headers=g5header,
                              callback=self.parse_detail,
                              meta={'date': sel_date, 'cycle': cycle, "dst": dst, "org": org, 'dacode': dacode})

    def parse_detail(self, response):
        try:
            ret = response.text
        except:
            self.spider_exception("IP Exception", "request CS flight detail error", errcode=-1)
            print response
            return
        etree_info = etree.HTML(ret)
        items = []
        for flight_div in xrange(1, 100):
            xpath_flightno = './/*[@id="dcFlightFlight"]/div[2]/ul/li[%d]/div/div[1]/div[1]/span[3]/label' % flight_div
            try:
                flightno = etree_info.find(xpath_flightno).text
                print flightno
            except Exception, e:
                break

            item = FlightSpiderBaseItem()
            item["company"] = "G5"
            item["flightNo"] = flightno
            item["season"] = 3
            list_code = response.meta["dacode"].split('-')
            item["depcode"] = list_code[0]
            item["arrcode"] = list_code[1]

            xpath_depPlanTime = './/*[@id="dcFlightFlight"]/div[2]/ul/li[%d]/div/div[2]/div[2]/form/' \
                                '*[@id="departuretime"]' % (flight_div)
            xpath_arrPlanTime = './/*[@id="dcFlightFlight"]/div[2]/ul/li[%d]/div/div[2]/div[2]/form/' \
                                '*[@id="arriveCityName"]' % (flight_div)
            dep_plantime = etree_info.find(xpath_depPlanTime).attrib
            arr_plantime = etree_info.find(xpath_arrPlanTime).attrib
            item["depPlanTime"] = '%s-%s' % (dep_plantime, arr_plantime)
            if item not in items:
                items.append(item)
        return items

    def spider_exception(self,reason, msg, errcode=-1):
        self.tmp_retry_times = errcode
        http_proxy.retry_http_proxy(self.hp_id)
        raise CloseSpider(reason)

