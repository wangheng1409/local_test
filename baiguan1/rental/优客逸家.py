# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='https://beijing.uoko.com/room/by0pg2/'

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    # 'Cookie': 'cityid=38; _gat=1; nTalk_CACHE_DATA={uid:kf_9452_ISME9754_guest03B2EB9E-FDDD-92,tid: 1509602984191746}; NTKF_T2D_CLIENTID=guest03B2EB9E-FDDD-920F-6CA8-7B5980FF9740; _ga=GA1.2.1798799815.1509602983; _gid=GA1.2.593414959.1509602983; Hm_lvt_9efdb82a30972ce34071a031946aa933=1509602984; Hm_lpvt_9efdb82a30972ce34071a031946aa933=1509603062',
    'Host': 'beijing.uoko.com',
    'Referer': 'https://beijing.uoko.com/room/by0/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

ret=requests.get(url,headers=headers,verify=False).text
print(ret)

