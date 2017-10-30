# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
r = redis.Redis(connection_pool=pool)
k='baishi_test_10w'
for i in range(211332004011,211332004011+10*10000):
    r.sadd(k,json.dumps(i))