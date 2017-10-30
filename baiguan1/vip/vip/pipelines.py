# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
import datetime, time
import redis
import json
from vip.util.RedisQueue import RedisQueue
from vip.items import VipItem

class VipPipeline(object):
    def __init__(self):
        if settings['TEST'] != True:
            self.client = pymongo.MongoClient(settings['LOCAL_MONGODB_URI'])
            # pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
        else:
            self.client = pymongo.MongoClient()
            # pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
        self.detail_handler = None
        self.db = self.client[settings['MONGODB_DB']]
        # self.redis_client = RedisQueue()
        # self.r = redis.Redis(connection_pool=pool)
    def process_item(self, item, spider):
        if not self.detail_handler:
            self.detail_handler = self.db[settings['MONGODB_DETAIL']]

        list_from_json = item['detail']
        list_from_json['ts_string'] = str(datetime.date.today())
        list_from_json['ts'] = str(datetime.datetime.fromtimestamp(time.time(), None))
        try:
            self.detail_handler.insert(list_from_json,check_keys=False)
        except Exception as e:
            print(e,[x for x in list_from_json.keys()])
