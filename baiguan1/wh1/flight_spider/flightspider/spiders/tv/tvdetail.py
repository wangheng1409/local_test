#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import urllib
import requests
import random
from lxml import etree

from scrapy.spiders import Spider
from scrapy.http.request import Request

from flightspider import database
from flightspider import settings
from flightspider.lib.tools import getdayofday
from flightspider.items import FlightSpiderDetailItem
from flightspider.spiders.base_spider import BaseSpider


class TvDetailSpider(BaseSpider):
    """
    西藏航空运价数据
    """
    name = "tvdetail"
    allowed_domains = ["http://www.tibetairlines.com.cn"]
    start_urls = "http://www.tibetairlines.com.cn/tibetair/book/flightQuery.do"
    code = 'TV'
    UG = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) "
        "Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 "
        "Safari/534.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) "
        "Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; "
        ".NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"]

    def start_requests(self):
        tasks = self.get_tasks(self.code)
        for task in tasks:
            depcode = task["depCode"]
            arrcode = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = '%s-%s' % (depcode, arrcode)
            for d in xrange(task["dateRange"]):
                # 计算有效航线
                user_agent = random.choice(self.UG)
                sel_date, week = getdayofday(d, True)
                if task["weeks"].find(week) < 0:
                    continue
                time.sleep(2.9)
                cookie_url = 'http://www.tibetairlines.com.cn/tibetair/index.jsp'
                session = requests.session()
		session.proxies = {
                    "http": self.http_proxy,
                }
                try:
                    rtn = session.get(cookie_url, timeout=15)
                except Exception, e:
                    print e
                    self.tmp_retry_times = -1
                    self.spider_exception(sel_date, dacode, "TV IP blocked", "TV IP blocked", exc="TV IP blocked")
                    break
                cookie = requests.utils.dict_from_cookiejar(rtn.cookies)
                header = {
                    "Host": "www.tibetairlines.com.cn",
                    "Connection": "keep-alive",
                    "User-Agent": user_agent,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Referer": "http://www.tibetairlines.com.cn/tibetair/book/flightQuery.do",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.8"
                }
                cookies = {
                    "AlteonP": cookie["AlteonP"],
                    "Webtrends": cookie["Webtrends"],
                    "JSESSIONID": cookie["JSESSIONID"],
                    "__ozlvd1833": str(int(time.time()))
                }
                name_list = task["name"].split('-')
                params = {
                    "depCityInput": "%s" % name_list[0].encode('utf-8'),
                    "depCity": "%s" % depcode,
                    "flightGoDate": "%s" % sel_date,
                    "adultNum": "1",
                    "typeTrip": "0",
                    "arrCityInput": "%s" % name_list[1].encode('utf-8'),
                    "arrCity": "%s" % arrcode,
                    "flightReturnDate": "2014-09-03",
                    "childNum": "0"
                }
                url_params = urllib.urlencode(params)
                url = 'http://www.tibetairlines.com.cn/tibetair/book/flightQuery.do'
                yield Request(url, method="POST", headers=header, body=url_params, cookies=cookies, callback=self.parse_detail,
                              meta={'date': sel_date, 'cycle': cycle, "depcode": depcode, "arrcode": arrcode,
                                    'dacode': dacode, 'proxy': self.http_proxy})

    def parse_detail(self, response):
        try:
            ret = response.text
            pos = ret.find(u'您的ip被系统自动屏蔽，请联系西藏航空客服')
            if pos != -1:
                print "您的ip被系统自动屏蔽，请联系西藏航空客服"
                self.tmp_retry_times = -1
                self.spider_exception(response.meta["date"], response.meta["dacode"], "TV IP blocked", exc="TV IP blocked")
            html_info = etree.HTML(ret)
        except:
            return
        tr_id = 2
        items = []
        while True:
            flightno = ''
            str_orgin = './/*[@id="book-write"]/div[1]/div[2]/div[2]/div[4]/div/table/tr[%d]/td[2]' % tr_id
            str_share = './/*[@id="book-write"]/div[1]/div[2]/div[2]/div[4]/div/table/tr[%d]/td[2]/span' % tr_id
            str_stop = '//*[@id="book-write"]/div[1]/div[2]/div[2]/div[4]/div/table/tr[%d]/td[5]/text()' % tr_id
            try:
                flightno = html_info.find(str_orgin).text.replace('\r\n', '').replace('\t', '').replace(' ', '')
            except:
                break
            # 过滤经停
            stop_info = html_info.xpath(str_stop)
            if stop_info[0].replace('\r\n', '').replace('\t', '').replace(' ', '') == u'经停':
                tr_id += 5
                continue
            try:
                rtn_share = html_info.find(str_share).text.replace('\r\n', '').replace('\t', '').replace(' ', '')
                if rtn_share == u'享':
                    share = 1
                    tr_id += 5
                    continue
            except:
                share = 0

            for td_id in xrange(6, 12):
                str_path = '//*[@id="book-write"]/div[1]/div[2]/div[2]/div[4]/div/table/tr[%d]/td[%d]' % (tr_id, td_id)
                try:
                    price = html_info.find('.' + str_path + '/b').text
                    pos = price.find('.')
                    price = price[1:pos]
                except:
                    continue
                cabin = html_info.find('.' + str_path + '/input').attrib["idno"][-1]
                surplus_ticket_list = html_info.xpath(str_path + '/text()')
                for item in surplus_ticket_list:
                    surplus_ticket = item.replace('\t', '').replace('\r\n', '').replace(' ', '')
                    if surplus_ticket == '':
                        continue
                    else:
                        break
                item = FlightSpiderDetailItem()
                item["company"] = 'TV'
                item["flightNo"] = flightno
                item["flightDate"] = response.meta["date"]
                item["cabinId"] = cabin
                item["depCode"] = response.meta["depcode"]
                item["arrCode"] = response.meta["arrcode"]
                item["price"] = price
                item["priceCurrency"] = 'CNY'
                item["surplusTicket"] = surplus_ticket
                item["share"] = share
                item["remarks"] = ""
                item["syncCycle"] = response.meta["cycle"]
                if item not in items:
                    items.append(item)

            for hidden_id in xrange(1, 13):
                str_hidden = '//*[@id="book-write"]/div[1]/div[2]/div[2]/div[4]/div/table' \
                             '/tr[%d]/td[2]/table/tr/td[%d]/text()' % (tr_id+2, hidden_id)
                lists = html_info.xpath(str_hidden)
                if len(lists):
                    cabin = lists[0].replace('\r\n', '').replace('\t', '').replace(' ', '')[:1]
                    price = lists[2].replace('\r\n', '').replace('\t', '').replace(' ', '')
                    pos = price.find('.')
                    price = price[1:pos]
                    surplus_ticket = lists[3].replace('\r\n', '').replace('\t', '').replace(' ', '')
                    item = FlightSpiderDetailItem()
                    item["company"] = 'TV'
                    item["flightNo"] = flightno
                    item["flightDate"] = response.meta["date"]
                    item["cabinId"] = cabin
                    item["depCode"] = response.meta["depcode"]
                    item["arrCode"] = response.meta["arrcode"]
                    item["price"] = price
                    item["priceCurrency"] = 'CNY'
                    item["surplusTicket"] = surplus_ticket
                    item["share"] = share
                    item["remarks"] = ""
                    item["syncCycle"] = response.meta["cycle"]
                    if item not in items:
                        items.append(item)
                else:
                    break
            tr_id += 5
        return items

