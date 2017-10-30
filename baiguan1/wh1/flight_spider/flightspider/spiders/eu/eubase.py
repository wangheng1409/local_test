#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import simplejson
import re
from bs4 import BeautifulSoup

from scrapy.spiders import Spider
from scrapy.http.request.form import FormRequest

from flightspider.items import FlightSpiderBaseItem
from flightspider import settings
from flightspider import database
from flightspider.lib.tools import getdayofday


class EuDetailSpider(Spider):
    """
    成都航空航班基础数据
    """
    name = "eubase"
    allowed_domains = ["http://b2c.chengduair.cc"]
    start_urls = "http://b2c.chengduair.cc/euair/reservation/flightQuery.do"

    def start_requests(self):
        # 根据配置文件worker获取从抓取策略获取任务
        # if self.task_id == -1:
        #     tasks = database.get_tasks(settings.WORKER, self.name, "EU")
        # else:
        #     tasks = database.get_tasks("", "", "", self.task_id)
        #     # 记录爬虫开始状态
        #     database.update_task_state(self.task_id, 2)
        tasks = database.get_tasks(settings.WORKER, "eudetail", "EU")
        print len(tasks)
        for task in tasks:
            dst = task["depCode"]
            org = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = task["name"]
            # 获取cookie
            url = 'http://b2c.chengduair.cc/euair/index.jsp'
            rtn = requests.get(url)
            dict_cookies = requests.utils.dict_from_cookiejar(rtn.cookies)

            for d in xrange(task["dateRange"]):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                if task["weeks"].find(week) < 0:
                    continue

                euheader = {
                    "Host": "b2c.chengduair.cc",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate",
                    "Referer": "http://b2c.chengduair.cc/euair/index.jsp",
                    "Cookie": "AlteonP=" + dict_cookies["AlteonP"] + ";"
                              "Webtrends=" + dict_cookies["Webtrends"] + ";"
                              "JSESSIONID=" + dict_cookies["JSESSIONID"],
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded",
                }
                url_info = "http://b2c.chengduair.cc/euair/reservation/flightQuery.do"

                data = {
                    "orgCity": "%s" % org,
                    "takeoffDate": "%s" % sel_date,
                    "tripType": "0",
                    "destCity": "%s" % dst,
                    "adultNum": "1",
                    "childNum": "0",
                    "babyNum": "0",
                }

                yield FormRequest(url_info, headers=euheader, formdata=data, callback=self.parse_detail,
                                  meta={'date': sel_date, 'cycle': cycle, "dst": dst, "org": org, 'dacode': dacode})

    def parse_detail(self, response):
        try:
            ret = response.text
        except:
            return
        pos_airline_over = ret.find(u'航班已销售完毕')
        if pos_airline_over == -1:
            soup = BeautifulSoup(ret, "html.parser")
            try:
                soup_tmp = soup.contents[2].contents[3].contents[25].contents[5].contents[1].contents[3].contents[13]
            except:
                print '错误的response:%s' % response
                return
            reg1 = re.compile("<[^>]*>")
            content = reg1.sub('', soup_tmp.prettify())
            str_info = content.strip()[130:].replace('\r', '').replace('\n', '').replace('\t', '')
            print str_info
            items = []
            while True:
                flightno_pos = str_info.find('EU')
                if flightno_pos == -1:
                    break
                flightno = str_info[flightno_pos:flightno_pos + 6]

                time_pos = str_info.find('-')
                plantime = str_info[time_pos - 5: time_pos + 6]
                plantime.replace(" ", "")
                # time_list = plantime.split('-')
                str_info = str_info[time_pos + 6:]

                item = FlightSpiderBaseItem()
                item['flightNo'] = flightno
                item['depcode'] = response.meta["dst"]
                item['arrcode'] = response.meta["org"]
                item['company'] = "EU"
                item['season'] = 3

                item['depPlanTime'] = plantime
                item['arrPlanTime'] = ""
                if item not in items:
                    items.append(item)
            return items
