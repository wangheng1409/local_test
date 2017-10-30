#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib

from lxml import etree
from scrapy.http.request import Request
from flightspider.lib.tools import getdayofday
from flightspider.items import FlightSpiderDetailItem
from flightspider.spiders.base_spider import BaseSpider


class G5DetailSpider(BaseSpider):
    """
    华夏航空运价数据
    """
    name = "g5detail"
    code = "G5"
    allowed_domains = ["http://www.chinaexpressair.com"]
    start_urls = "http://www.chinaexpressair.com/flight.ac?"

    def start_requests(self):
        tasks = self.get_tasks(self.code)
        for task in tasks:
            dst = task["depCode"]
            org = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = '%s-%s' % (dst, org)
            dst_city, org_city = task["name"].split('-')

            url_jsessionid = 'http://www.chinaexpressair.com/'
            # 重试次数
            retry_num = 1
            while True:
                res = requests.get(url_jsessionid, timeout=10)
                res_cookie = requests.utils.dict_from_cookiejar(res.cookies)
                if res_cookie["JSESSIONID"]:
                    break
                if retry_num == 3:
                    return
                retry_num += 1

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
        except Exception, e:
            self.spider_exception(response.meta["date"], response.meta["dacode"], "G5 response Exception", exc=e.message)
            return
        etree_info = etree.HTML(ret)
        items = []
        for flight_div in xrange(1, 100):
            xpath_flightno = './/*[@id="dcFlightFlight"]/div[2]/ul/li[%d]/div/div[1]/div[1]/span[3]/label' % flight_div
            try:
                flightno = etree_info.find(xpath_flightno).text
            except Exception, e:
                #self.spider_exception(response.meta["date"], response.meta["dacode"], "G5 html parse Exception",
                #                      exc=e.message)
                break
            for input_radio in xrange(2, 5):
                item = FlightSpiderDetailItem()
                item["company"] = "G5"
                item["flightNo"] = flightno
                item["flightDate"] = response.meta["date"]

                xpath_cabin = './/*[@id="dcFlightFlight"]/div[2]/ul/li[%d]/div/div[%d]/div[2]/form/' \
                              '*[@id="code"]' % (flight_div, input_radio)

                try:
                    dict_cabin_attrib = etree_info.find(xpath_cabin).attrib
                except:
                    # print '已售罄'
                    continue

                cabin = dict_cabin_attrib["value"]
                item["cabinId"] = cabin
                item["depCode"] = response.meta["dst"]
                item["arrCode"] = response.meta["org"]

                xpath_price = './/*[@id="dcFlightFlight"]/div[2]/ul/li[%d]/div/div[%d]/div[2]/form/' \
                              '*[@id="price"]' % (flight_div, input_radio)

                dict_price_attrib = etree_info.find(xpath_price).attrib
                price = dict_price_attrib["value"]
                item["price"] = price

                # 华夏航空官网未标明货币类型
                item["priceCurrency"] = 'CNY'
                # 华夏航空官网没有标明余票,客服确认,确实不提供余票信息,余票信息只能通过打电话的方式获得.
                item["surplusTicket"] = 'A'
                item["remarks"] = ''
                item["syncCycle"] = response.meta["cycle"]

                xpath_share = './/*[@id="dcFlightFlight"]/div[2]/ul/li[%d]/div/div[%d]/div[2]/form/' \
                              '*[@id="shareflight"]' % (flight_div, input_radio)
                dict_share_attrib = etree_info.find(xpath_share).attrib
                str_share = dict_share_attrib["value"]
                if str_share == "":
                    share = 0
                else:
                    share = 1
                item["share"] = share
                if item not in items:
                    items.append(item)
        return items


