# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import random

url="https://restapi.ele.me/shopping/v1/restaurants/5331948432112129/business/qualification"
url="https://restapi.ele.me/shopping/v1/restaurants/6311948457994129/business/qualification"
# s=list('5331948432112129')
# random.shuffle(s)
# s=''.join(s)
# url='https://restapi.ele.me/shopping/v1/restaurants/'+s+'/business/qualification'
# print url

headers={
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Cookie':'_utrace=91a0fddf1a3af29e08ed00c5e12d215c_2017-11-24; ubt_ssid=60cm979qpiyrn27ugmtfp65teddfow2t_2017-11-24; perf_ssid=rt4gtak1wvymihcnp9ywu8is345te1ao_2017-11-24',
'Host':'restapi.ele.me',
'Origin':'https://h5.ele.me',
'Referer':'https://h5.ele.me/shop/certification/',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
'X-Shard':'shopid=156121984;loc=121.53497,31.21339',
}

ret=requests.get(url,headers=headers).text
print ret