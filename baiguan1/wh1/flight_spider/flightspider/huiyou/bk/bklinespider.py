#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
from scrapy.http.request import Request

line_list=[]
class DmozSpider(scrapy.spiders.Spider):
    name = "bkline"
    allowed_domains = [""]
    start_urls = ""

    def start_requests(self):
        for i in range(11,18):
            url='http://www.variflight.com/embed/okair/flightschedule.asp?page='+str(i)
            yield  Request(url, callback = self.parse)

    def parse(self, response):
        print 1
        for sel in response.xpath('//*[@id="rightcon"]/div/div[2]/table/tr')[1:-1]:
            start=sel.xpath('.//td[4]/text()').extract()[0]
            end=sel.xpath('.//td[5]/text()').extract()[0]
            line_list.append(start+'-'+end)
        print set(line_list)


