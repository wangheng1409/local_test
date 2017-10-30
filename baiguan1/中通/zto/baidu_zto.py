# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import pandas as pd


id_pd = pd.read_csv('baidu_order.csv', header=0, sep=',')
# print(id_pd)
s=id_pd['oid'].values.tolist()
print(len(s),len(set(s)))


# import redis
#
# pool = redis.ConnectionPool(host='60.205.152.167', port='6379', db='0', password='bigone2016')
# r = redis.Redis(connection_pool=pool)
# for i in s:
#     r.sadd('baidu_zto', json.dumps(i))