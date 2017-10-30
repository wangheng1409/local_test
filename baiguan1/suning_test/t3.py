# !/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import json
from bo_lib.general.mongodb_helper import MongoDBHelper

mongoDBHelper = MongoDBHelper()
collection = mongoDBHelper.get_collection(collection_name='suning_detail', database_name='suning')

s=collection.distinct('salesCode',{'ts_string':{'$gte':'2017-10-05','$lte':'2017-10-06'}},allowDiskUse=True )

s=list(s)
print(len(s))

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
r = redis.Redis(connection_pool=pool)
for store_id in s:
    r.lpush('suning_store_id',json.dumps(store_id))

