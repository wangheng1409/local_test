# !/usr/bin/env python
# -*- coding:utf-8 -*-

from bo_lib.general.redis_helper import RedisHelper
r = RedisHelper().client
k=str(0)
with open('./sto_data/f'+k+'.txt','rb') as f:
    for line in f:
        r.sadd('sto_'+k,line.decode().strip())