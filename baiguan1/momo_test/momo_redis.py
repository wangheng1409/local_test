# !/usr/bin/env python
# -*- coding:utf-8 -*-

from bo_lib.general.redis_helper import RedisHelper
r = RedisHelper().client
k=str(0)
with open('./momo_paying_user_data/f'+k+'.txt','rb') as f:
    for line in f:
        r.sadd('momo_paying_user_'+k,line.decode().strip())