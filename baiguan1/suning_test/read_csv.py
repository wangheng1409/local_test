# !/usr/bin/env python
# -*- coding:utf-8 -*-
'''
"catentry_id","countofarticle","totalcount","store_id"
'''
import pandas as pd
import redis
import time
import datetime
import json
import requests
import pymongo
from bo_lib.general import ProxyManager
pm = ProxyManager()

client = pymongo.MongoClient('mongodb://root:big_one_112358@123.59.69.66:5600')
# client = pymongo.MongoClient()
db = client['suning']
collection = db.comment_page1

has_complete=set(collection.distinct('catentry_id'))
print(len(has_complete))

# pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
# r = redis.Redis(connection_pool=pool)

id_pd = pd.read_csv('suning_store.csv', header=0, sep=',')
# print(id_pd)
store_id = id_pd['store_id'].values.tolist()

# print(s)
catentry_id = id_pd['catentry_id'].values.tolist()
print(len(catentry_id))

print(len(catentry_id)-len(has_complete))
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Host': 'review.suning.com',
    'If-Modified-Since': 'Fri, 27 Oct 2017 06:50: 24 GMT',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
}
for k, v in zip(store_id, catentry_id):
    if v in has_complete:
        continue
    # r.lpush('suning_comment_page1', json.dumps(('00' + str(k), str(v))))
    url = 'http://review.suning.com/ajax/review_lists/general-000000000' + str(v) + '-' + str(
        '00' + str(k)) + '-total-1-default-10-----reviewList.htm?callback=reviewList'
    s=requests.get(url,headers=header, proxies=pm.getProxyV2()).text

    try:
        left = s.index('{')
        ret = s.strip()[left:-1]
        ret_dic = json.loads(ret)
        print('store_id, catentry_id:',k, v,'success')
    except:
        continue
    for comment in ret_dic['commodityReviews']:
        comment['store_id'] = k
        comment['catentry_id'] = v
        comment['ts_string'] = str(datetime.date.today())
        comment['ts'] = str(datetime.datetime.fromtimestamp(time.time(), None))
        collection.insert(comment, check_keys=False)

