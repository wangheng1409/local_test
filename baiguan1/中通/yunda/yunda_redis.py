# !/usr/bin/env python
# -*- coding:utf-8 -*-

from bo_lib.general.redis_helper import RedisHelper

r = RedisHelper().client
k=str(2)
with open('./yunda_data/f'+k+'.txt','rb') as f:
    for line in f:
        r.sadd('yunda_'+k,line.decode().strip())