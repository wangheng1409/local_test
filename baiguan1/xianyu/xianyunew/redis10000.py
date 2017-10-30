# !/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import pymongo
import json
import random

TEST=False
redis_key = 'xianyu_item_10000'

if not TEST:
    pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
else:
    pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
r = redis.Redis(connection_pool=pool)

client = pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
db = client.xianyu.xianyu_detail2

catagory_dic = {
            '50100408': '家用电器',
            '50100406': '居家日用',
            '50100409': '母婴',
            '50100405': '美容/美颜/香水',
            '50100398': '手机',
            '50100401': '相机/摄像机',
            '50100402': '笔记本电脑/电脑周边',
            '50100403': '随身影音娱乐',
            '50100411': '卡券/文体/户外/宠物',
            '50446013': '女装',
            '50100415': '珠宝/收藏',
            '50448012': '鞋包配饰',
        }

catagory_num={
    '50100408': 169,
    '50100406': 351,
    '50100409': 381,
    '50100405': 538,
    '50100398': 246,
    '50100401': 21,
    '50100402': 51,
    '50100403': 39,
    '50100411': 40,
    '50446013': 4296,
    '50100415': 195,
    '50448012': 3675,

}
for cat_id,cat_num in zip(catagory_dic,catagory_num.values()):
    item_id_list=db.distinct('itemid',{'catid':cat_id})
    random.shuffle(item_id_list)
    print(len(item_id_list))
    item_id_list=item_id_list[:cat_num]
    for item_id in item_id_list:

        r.lpush(redis_key,json.dumps(str(item_id)))