# !/usr/bin/env python
# -*- coding:utf-8 -*-

from bo_lib.general.redis_helper import RedisHelper


r = RedisHelper().client
r.sadd('wangheng_test_redishelper','123')