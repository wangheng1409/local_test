# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
import redis
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
from kuaidige.items import KuaidigeItem
from kuaidige.before.before import headers

#start：
        # "latitude": "39.260",      "latitude": "41.030",
        # "longitude": "115.250",    "longitude": "117.300",

# CITY_DICT={
#     '北京':[(39260,41030),(115250,117300)],
#     '上海':[(30400,31530),(120510,122120)],
#     '广州':[(22260,23560),(112570,114030)],
#     '深圳':[(22270,22520),(113460,114370)],
# }
CITY_DICT={
    'part1':[(18156,42130),(100711,123000)],
    'part2':[(38828,52988),(119010,134171)],
}
class StockSpider(RedisSpider):
    name = "kuaidigespider"
    allowed_domains = []

    def start_requests(self):
        for city,v in CITY_DICT.items():
            for x in range(v[0][0],v[0][1],5):
                for y in range(v[1][0], v[1][1],5):
                    latitude=str(x)[:2]+'.'+str(x)[2:]
                    longitude=str(y)[:3]+'.'+str(y)[3:]
                    url, header, data = headers(latitude, longitude)
                    print( latitude, longitude)
                    yield scrapy.FormRequest(url,
                                              formdata=data,
                                              headers=header,
                                              meta={'city': city,
                                                    'latitude':latitude,
                                                    'longitude':longitude,

                                                },
                                              dont_filter=True)


    def parse(self, response):
        city = response.meta['city']
        latitude = response.meta['latitude']
        longitude = response.meta['longitude']
        print('s')
        storemenu_json = response.body.decode()
        try:
            storemenu = json.loads(storemenu_json)
            print('storemenu:',storemenu)
        except Exception:
            self.retry_this_poi({'city': city,'latitude': latitude,'longitude': longitude,
                                 })
            self.logger.warning(
                '%s：%s,%s抓取失败，已放回redis等待下次重新抓取' % (city,latitude,longitude))
            return

        if not isinstance(storemenu, dict):
            self.retry_this_poi({'city': city,'latitude': latitude,'longitude': longitude, })
            self.logger.warning(
                '%s：%s,%s抓取失败，已放回redis等待下次重新抓取' % (city,latitude,longitude))
            return
        if not storemenu['coList']:
            return

        item = KuaidigeItem()
        for poi in storemenu['coList']:
            poi['cityName']=city
            item['detail'] = poi
            yield item

    def retry_this_poi(self, dic):
        # self.r.sadd('set' + self.redis_key, json.dumps(dic).encode("utf-8"))
        pass
