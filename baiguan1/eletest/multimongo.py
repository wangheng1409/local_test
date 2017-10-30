# !/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import pymongo
import time
from bson import ObjectId
from concurrent.futures import ThreadPoolExecutor, as_completed
from pympler import summary
from pympler import muppy
import gc
import copy


class MultiMongo():
    def __init__(self,find_condition_dic,keywords_dic=None,mongouri='***',
                 database='shengjian',collection='store_list'):
        self.collection=pymongo.MongoClient(mongouri)[database][collection]
        self.find_condition_dic = find_condition_dic
        self.keywords_dic = keywords_dic
        self.start_timestamp=self.oid_to_timestamp(self.get_start_objectid()) if 'ts_string' not in self.find_condition_dic else\
            self.oid_to_timestamp(str(int(time.mktime(time.strptime(self.find_condition_dic['ts_string'], "%Y-%m-%d")))))
        self.end_timestamp=self.oid_to_timestamp(self.get_end_objectid())
        print(self.start_timestamp,self.end_timestamp)
        self.result=[]

    def object_id(self,timestamp):
        return ObjectId(str(hex(timestamp))[2:] + 16 * '0')

    def get_start_objectid(self):
        return str(self.collection.find_one()['_id'])[:8]

    def get_end_objectid(self):
        return str([x for x in self.collection.find({}).sort('_id',pymongo.DESCENDING).limit(1)][0]['_id'])[:8]

    def oid_to_timestamp(self,oid):
        oid='0x'+oid
        return int(oid, 16)

    def cut_timestamp(self,start,end):
        return [x for x in range(start,end,86400)]+[end]

    def find(self):
        oid_list=[self.object_id(x) for x in self.cut_timestamp(self.start_timestamp,self.end_timestamp)]
        new_oid_list=[(oid_list[i],oid_list[i+1]) for i in range(len(oid_list)-1)]
        for cycle in self.gen_executor(self.find_detail, new_oid_list):
            gc.collect()
            # summary.print_(summary.summarize(muppy.get_objects()), limit=4)
        return (x for y in self.result for x in y)

    def find_detail(self,item):
        start = item[0]
        end = item[1]
        append_condition = {'_id': {'$gte': start, '$lt': end}}
        find_condition=copy.deepcopy(self.find_condition_dic)
        find_condition.update(append_condition)
        if self.keywords_dic:
            self.result.append(self.collection.find(find_condition, self.keywords_dic))
        else:
            self.result.append(self.collection.find(find_condition))

    def gen_executor(self,work, slice_list):
        workers = 10
        with ThreadPoolExecutor(workers) as executor:
            futures = [executor.submit(work, slice_item) for slice_item in slice_list]
            for future in as_completed(futures):
                futures.remove(future)
                yield

st2=time.time()
# mongo_obj=MultiMongo({'id':str(datetime.date.today())},{'id':1})
mongo_obj=MultiMongo({'fixed':1},{'id':1})

s=mongo_obj.find()
print(s)
print(time.time()-st2)


