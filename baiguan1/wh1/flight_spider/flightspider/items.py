#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

import scrapy


class FlightSpiderBaseItem(scrapy.Item):
    flightNo = scrapy.Field()
    depcode = scrapy.Field()
    arrcode = scrapy.Field()
    company = scrapy.Field()
    season = scrapy.Field()
    depPlanTime = scrapy.Field()
    arrPlanTime = scrapy.Field()


class FlightSpiderDetailItem(scrapy.Item):
    flightNo = scrapy.Field()       #航班号
    flightDate = scrapy.Field()     #航班日期
    cabinId = scrapy.Field()        #舱位
    depCode = scrapy.Field()        #出发地
    arrCode = scrapy.Field()        #目的地
    price = scrapy.Field()          #票价
    vipPrice = scrapy.Field()       #东航会员价格
    priceCurrency = scrapy.Field()  #票价币种
    surplusTicket = scrapy.Field()  #余票
    share = scrapy.Field()          #是否为共享航班
    remarks = scrapy.Field()        #描述
    syncCycle = scrapy.Field()      #抓取周期
    company = scrapy.Field()        #航空公司名
