# !/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import requests
import time
url='http://weixin.wowqu.com.cn/api/innSearchCtrl/innsSearch?' \
    'topRent=100000&lowRent=0&' \
    'distance=&' \
    'zoneLng=&' \
    'zoneLat=&' \
    'keyWords=&' \
    'cityCode=AR06513&' \
    'lng=&lat=&brandId='

headers={
    'Host': 'weixin.wowqu.com.cn',
    'Referer': 'http://weixin.wowqu.com.cn/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/zh_CN',
}

ret=requests.get(url,headers=headers).text
print(ret)

