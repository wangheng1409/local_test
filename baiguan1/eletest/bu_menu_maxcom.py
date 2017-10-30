# -*- coding: utf-8 -*-

import sys
from datahub import DataHub
from datahub.models import RecordType, TupleRecord
from pymongo import MongoClient
from bson import ObjectId
import threading
import Queue
import time
import pymysql

# uri = 'mongodb://root:Baiguan2016@60.205.152.167:3717'
uri = 'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521'
mongo = MongoClient(uri)
db = mongo['shengjian']['store_menu_list']
access_id = 'LTAIypzOElY3tnVG'
access_key = 'kxR8s0VfwCzuh7atsLt3DEAqe5tnuf'
endpoint = 'http://dh-cn-hangzhou.aliyuncs.com'
dh = DataHub(access_id, access_key, endpoint)
project_name = 'kysj_2mc'
topic_name = 'sj_menu'


class Sj2MSync(threading.Thread):
    def __init__(self, shard_num):
        threading.Thread.__init__(self)
        self.shard_num = shard_num

    def run(self):
        while not slice_queue.empty():
            current_slice = slice_queue.get()
            if current_slice:
                self.query(current_slice)
        print('shard: {} finished.'.format(self.shard_num))

    def query(self, start_object_id_int):
        records = []
        conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj',
                               charset='utf8')
        # 创建游标
        cursor = conn.cursor()
        cursor.execute("select poi_id from waimai_poi where source=2 and insert_ts='2017-07-27'  and gmv is  null")
        ret = cursor.fetchall()

        for item in ret:
            store_id=item[0]
            row = db.find({'id': store_id},
                                 {'_id': 1,
                                  'specfoods': 1,
                                  'store_id': 1,
                                  'item_id': 1,
                                  'ts_string': 1
                                  })
            row=[x for x in row][0] if [x for x in row] else ''
            if not row:
                continue
            try:
                if 'ts_string' not in row:
                    ts_str = '2017-01-01'
                else:
                    ts_str = row['ts_string']
                    # ts_str = 'test'
                poi_id = row['store_id']
                item_id = row['item_id']

                for food in row['specfoods']:
                    rec = TupleRecord(schema=topic.record_schema)
                    rec['poi_id'] = poi_id
                    rec['id'] = item_id
                    rec['food_id'] = food['food_id']
                    rec['name'] = food['name']
                    rec['month_saled'] = food['recent_popularity']
                    rec['price'] = food['price']
                    rec['box_price'] = food['packing_fee']
                    rec['ts_string'] = ts_str
                    rec.shard_id = shards[self.shard_num].shard_id
                    records.append(rec)
            except Exception as e:
                print e
                continue
        if not records:
            print 'records is empty.'
            return
        item_queue.put(records)


class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            records = item_queue.get(True)
            if records:
                while self.upload(records):
                    time.sleep(2)

    def upload(self, records):
        try:
            failed_indexs = dh.put_records(project_name, topic_name, records)
            print "put tuple %d records, failed list: %s" % (len(records), failed_indexs)
            # print "put tuple %d records, failed list: %s" % (len(records), 0)
        except Exception as e:
            print 'ERROR：put_records：', e


def dispatch():
    start = int(s_oid, 16)
    end = int(e_oid, 16)
    slice_list = [x for x in range(start, end, 10)] #every 20 seconds means about 10000 rows
    return slice_list

if __name__ == '__main__':
    s_oid = sys.argv[1]
    e_oid = sys.argv[2]

    dh.wait_shards_ready(project_name, topic_name)
    print "shards all ready!"
    print "=======================================\n\n"

    topic = dh.get_topic(topic_name, project_name)
    print "get topic suc! topic=%s" % str(topic)
    if topic.record_type != RecordType.TUPLE:
        print "topic type illegal!"
        sys.exit(-1)
    shards = dh.list_shards(project_name, topic_name)
    shards_len = len(shards)
    print "=======================================\n\n"

    slice_queue = Queue.Queue()
    item_queue = Queue.Queue()
    for each in dispatch():
        slice_queue.put(each)

    for i in range(shards_len):
        consumer = Consumer()
        consumer.start()

    thread_list = []
    for i in range(shards_len):
        sync = Sj2MSync(i)
        sync.start()
        thread_list.append(sync)

    while len(thread_list) != 0:
        thread_list = [thread for thread in thread_list if thread.is_alive()]
        time.sleep(60)