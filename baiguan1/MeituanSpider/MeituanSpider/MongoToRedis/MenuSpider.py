# -*- coding:utf-8 -*-
from pymongo import MongoClient
import redis
import json


class AutoCatchTaskInfoCrawler(object):
    def __init__(self):
        pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
        self.r = redis.Redis(connection_pool=pool)
        #加载mongo配置
        self.client = MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
        self.db = self.client

    def get_db(self,name):
        return self.db[name]

    def get_collection(self,db,name):
        collection = db[name]
        return collection

    def update_task_info_status(self):
        print('update task info status')

    def catch_task_info(self):
        db = self.get_db('Meituan')
        res = db.get_collection('POI_BY_BUILDING').find({},{'_id':0,'id':1,'longitude':1,'latitude':1})
        for item in res:
            print(item)
            self.push_task_info_to_redis('MenuSpider',item)


    def push_task_info_to_redis(self,key,value):
        # 循环写入redis key-value
        self.r.sadd(key,json.dumps(value))

if __name__ == '__main__':
    actic = AutoCatchTaskInfoCrawler()
    actic.catch_task_info()