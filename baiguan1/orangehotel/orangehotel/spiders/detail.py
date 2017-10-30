# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
import redis
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
from orangehotel.items import OrangehotelItem




class StockSpider(RedisSpider):
    name = "oriangespider"
    allowed_domains = []
    start_urls = []

    def start_requests(self):
        yield scrapy.Request(url='http://www.orangehotel.com.cn/', callback=self.parse, dont_filter=True)

    def parse(self, response):  # 遍历所有的城市
        print(123)
        for city_ur,cityname in zip(response.xpath('//div[@id="cityList"]//a/@href').extract(),response.xpath('//div[@id="cityList"]//a/text()').extract()):
            column_ur = 'http://www.orangehotel.com.cn' + city_ur
            print('city_ur', column_ur,cityname)
            yield scrapy.Request(url=column_ur, callback=self.get_column, dont_filter=True, meta={'cityname':cityname})

    def get_column(self, response):  # 遍历所有的酒店
        cityname=response.meta['cityname']
        for hotel in response.xpath('//div[@id="pageWarp"]//section'):
            s={}
            s['city']=cityname
            s['name']=hotel.xpath('./div[@class="info-post"]/h2/a/text()').extract()[0]
            s['phone']=hotel.xpath('./div[@class="info-post"]/h3/text()').extract()[0].split('：')[1]
            s['desc']=hotel.xpath('./div[@class="info-post"]/div/p[1]/text()').extract()[0]
            s['address']=hotel.xpath('./div[@class="info-post"]/div/p[2]/text()').extract()[0].split('：')[1]
            s['url']='http://www.orangehotel.com.cn'+hotel.xpath('.//div[@class="img-wrap"]/a/@href').extract()[0]
            s['room']=[]
            for room in hotel.xpath('.//ul[@class="room_info"]')[1:]:
                t={}
                t['room_name']=room.xpath('./li[@class="li_roomname"]/text()').extract()[0]
                t['price']=room.xpath('./li[@class="p_line1"]/text()').extract()[0]
                t['first_price']=room.xpath('./li[3]/text()').extract()[0]
                t['has_room']=room.xpath('./li[4]//font/text()').extract()[0]
                s['room'].append(t)
            item = OrangehotelItem()
            item['detail'] = s
            yield item

    def retry_this_poi(self, dic):
        # self.r.sadd('set' + self.redis_key, json.dumps(dic).encode("utf-8"))
        pass
