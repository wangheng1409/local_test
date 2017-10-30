# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
import redis
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
from us_stock.items import UsStockItem
from us_stock.before.before import headers

URL_DICT={'yy':'133672',
          'momo':'175032'
          }
class StockSpider(RedisSpider):
    name = "stockspider"
    allowed_domains = []
    redis_key = 'stockspider'
    if not settings['TEST']:
        pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
    else:
        pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
    r = redis.Redis(connection_pool=pool)

    def start_requests(self):
        for name,item_id in URL_DICT.items():

            url, header = headers(item_id, 1)
            yield scrapy.Request(url, method="GET", headers=header,
                                  callback=self.parse,
                                  dont_filter=True,
                                  meta={'name': name,
                                        'item_id':item_id,
                                        'page': 1,
                                        }
                                  )

    def parse(self, response):
        name = response.meta['name']
        item_id = response.meta['item_id']
        page = response.meta['page']
        print('s')
        storemenu_json = response.body.decode()
        try:
            storemenu = json.loads(storemenu_json)
        except Exception:
            self.retry_this_poi({'name': name,
                                 'item_id': item_id,
                                 'page': page, })
            self.logger.warning(
                '%s：page%s抓取失败，已放回redis等待下次重新抓取' % (name,page))
            return

        if not isinstance(storemenu, dict):
            self.retry_this_poi({'name': name,
                                 'item_id': item_id,
                                 'page': page, })
            self.logger.warning(
                '%s：page%s抓取失败，已放回redis等待下次重新抓取' % (name, page))
            return

        item = UsStockItem()
        for poi in storemenu['rows']:
            poi['item_name']=name
            poi['item_id']=item_id
            item['detail'] = poi
            yield item
        if storemenu['page']<storemenu['total']:
            page+=1
            url, header = headers(item_id, page)
            yield scrapy.Request(url, method="GET", headers=header,
                                 callback=self.parse,
                                 dont_filter=True,
                                 meta={'name': name,
                                       'item_id': item_id,
                                       'page': page,
                                       }
                                 )
    def retry_this_poi(self, dic):
        self.r.sadd('set' + self.redis_key, json.dumps(dic).encode("utf-8"))
