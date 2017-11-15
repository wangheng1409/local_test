# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://www.h2ome.cn/api/c/search/rooms'

headers={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'csrftoken=b5wmsay5xFSxo9G8vQ949McgUBe62Di9; Hm_lvt_6c419ae441f286ef1a23fc9aa80a26e8=1509602355,1509602412; Hm_lpvt_6c419ae441f286ef1a23fc9aa80a26e8=1509602415',
    'Host': 'www.h2ome.cn',
    'Origin': 'http://www.h2ome.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.h2ome.cn/search?city=21&key=',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

data={
    'key':'',
    'city':'21',
    'district':'',
    'town':'',
    'metro':'',
    'bedrooms':'',
    'features':'',
    'price_low':'500',
    'price_high':'6000',
    'floor':'',
    'orientation':'',
    'style':'',
    'order_by':'',
    'entire':'',
    'page':'3',
    'csrfmiddlewaretoken':'b5wmsay5xFSxo9G8vQ949McgUBe62Di9',
}

ret=requests.post(url,headers=headers,data=data).text
print(ret)





