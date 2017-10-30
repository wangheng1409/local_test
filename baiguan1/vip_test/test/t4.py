#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pymongo
import redis
import json
import random


MONGODB_URI = 'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521'
LOCAL_MONGODB_URI = 'mongodb://root:Baiguan2016@60.205.152.167:3717'
Test=False

class AutoCatchTaskInfoCrawler(object):
    def __init__(self,):

        # 加载mongo配置
        if not Test:
            self.client = pymongo.MongoClient(MONGODB_URI)
            pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
        else:
            self.client = pymongo.MongoClient(LOCAL_MONGODB_URI)
            pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
        self.r = redis.Redis(connection_pool=pool)
        self.db = self.client

    def get_db(self,name):
        return self.db[name]

    def get_collection(self,db,name):
        collection = db[name]
        return collection

    def update_task_info_status(self):
        print('update task info status')

    def catch_task_info(self):
        # db = self.get_db('shengjian')
        # res = db.get_collection('store_list').find({},{'_id':0,'id':1,'latitude':1,'longitude':1})
        # for item in res:
        #     print(item)
        #     self.push_task_info_to_redis('storecommentspider',item)
        for i in range(1,11):
            key='zto_set'+str(i)
            while self.r.scard(key) < 10000000:
                res=self.r.spop('zto_set0')
                if self.r.scard(key)%10000==0:
                    print(0,self.r.scard(key))
                self.r.sadd(key, res)

    def push_task_info_to_redis(self,key,value):
        # 循环写入redis key-value
        self.r.lpush(key,value)
    def oid_generator(self,key):
        res = random.choice(['4','7','5'])+"%0.11d" % random.randint(0, 99999999999)
        if len(str(int(res)))==12:
            self.r.sadd(key, res)

if __name__ == '__main__':
    actic = AutoCatchTaskInfoCrawler()
    actic.catch_task_info()