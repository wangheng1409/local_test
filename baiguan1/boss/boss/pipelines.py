# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo
import datetime, time
import redis
from boss.util.RedisQueue import RedisQueue
from boss.items import BossItem,BossCompanyItem,BossniuItem


class BossPipeline(object):
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
        if isinstance(item, BossItem):
            self.process_detail(item)
        elif isinstance(item, BossCompanyItem):
            self.process_company(item)
        elif isinstance(item, BossniuItem):
            self.process_niu(item)
        return item
    def process_detail(self, item):

        self.detail_handler = self.db[settings['MONGODB_DETAIL']]
        list_from_json = item['detail']
        list_from_json['ts_string'] = str(datetime.date.today())
        list_from_json['ts'] = datetime.datetime.fromtimestamp(time.time(), None)
        self.detail_handler.insert(list_from_json)

    def process_company(self, item):

        self.detail_handler = self.db[settings['MONGODB_COMPANY']]

        list_from_json = item['detail']
        list_from_json['ts_string'] = str(datetime.date.today())
        list_from_json['ts'] = datetime.datetime.fromtimestamp(time.time(), None)
        self.detail_handler.insert(list_from_json)
    def process_niu(self, item):

        self.detail_handler = self.db[settings['MONGODB_NIU']]

        list_from_json = item['detail']
        list_from_json['ts_string'] = str(datetime.date.today())
        list_from_json['ts'] = datetime.datetime.fromtimestamp(time.time(), None)
        self.detail_handler.insert(list_from_json)