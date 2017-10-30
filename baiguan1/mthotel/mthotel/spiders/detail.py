# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
import redis
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
from mthotel.items import MthotelItem
from mthotel.before.before import headers

CITY_LIST=[
            # 'beijing',
           # 'shanghai',
           # 'guangzhou',
           # 'shenzhen',
           # 'shenyang',
           # 'jinan',
           # 'hangzhou',
           # 'nanjing',
           # 'hefei',
           # 'taiyuan',
           # 'fuzhou',
           # 'changsha',
           # 'chengdu',
           # 'shijiazhuang',
           # 'huizhou',
           # 'quanzhou',
           'nanchang',
           # 'kaifeng',
           # 'nantong',
           # 'jinhua',
           ]
class StockSpider(RedisSpider):
    name = "mthotelspider"
    allowed_domains = []
    # redis_key = 'mthotelspider'
    # if not settings['TEST']:
    #     pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
    # else:
    #     pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
    # r = redis.Redis(connection_pool=pool)

    def start_requests(self):
        for city in CITY_LIST:
            url, header = headers(1, city)
            yield scrapy.Request(url, method="GET", headers=header,
                                  callback=self.parse,
                                  dont_filter=True,
                                  meta={'city': city,
                                        'page': 1,
                                        }
                                  )

    def parse(self, response):
        city = response.meta['city']
        page = response.meta['page']
        print('s')
        storemenu_json = response.body.decode()
        try:
            storemenu = json.loads(storemenu_json)
            print('storemenu:',storemenu)
        except Exception:
            self.retry_this_poi({'city': city,
                                 'page': page, })
            self.logger.warning(
                '%s：page%s抓取失败，已放回redis等待下次重新抓取' % (city,page))
            return

        if not isinstance(storemenu, dict):
            self.retry_this_poi({'city': city,
                                 'page': page, })
            self.logger.warning(
                '%s：page%s抓取失败，已放回redis等待下次重新抓取' % (city, page))
            return
        if storemenu['data']['noResult']:
            return

        item = MthotelItem()
        for poi in storemenu['data']['poiInfo']:
            poi['cityName']=storemenu['data']['cityName']
            poi['poiPrice']=storemenu['data']['poiDealList'][str(poi['poiID'])]['poiPrice']
            poi['dealIDList']=[x for x in map(lambda item:storemenu['data']['dealsData'][str(item)],storemenu['data']['poiDealList'][str(poi['poiID'])]['dealIDList'])]


            item['detail'] = poi
            yield item
        if not storemenu['data']['noResult']:
            page+=1
            url, header = headers(page, city)
            yield scrapy.Request(url, method="GET", headers=header,
                                 callback=self.parse,
                                 dont_filter=True,
                                 meta={'city': city,
                                       'page': page,
                                       }
                                 )
    def retry_this_poi(self, dic):
        # self.r.sadd('set' + self.redis_key, json.dumps(dic).encode("utf-8"))
        pass
