# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://120.76.168.100:51001/v2/item/room_type/get_list_4_web'

headers={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': '120.76.168.100:51001',
    'Origin': 'http://apartment.luxgems.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://apartment.luxgems.com/qy/pc_new/longList.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

data={
    'data':json.dumps({"params":{"pageNo":3,"pageSize":"6","gcid":"888888","projectId":"","houseTypeId":"","cityId":"","pinpai":"","minPrice":"","maxPrice":""}})
}

ret=requests.post(url,headers=headers,data=data).text
print(ret)





