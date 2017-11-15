# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://sh.ziroom.com/index.php?_p=map&_a=rooms'

headers={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'PHPSESSID=ousgdcu58b1kricdr29mfq7gr5; CURRENT_CITY_CODE=440300; CURRENT_CITY_NAME=%E6%B7%B1%E5%9C%B3; gr_user_id=c547ba0c-6320-4f75-84ba-f6ead3976ffc; gr_session_id_8da2730aaedd7628=c46f27af-b74c-41c4-9e10-bd3a99830fda',
    'Host': 'sz.ziroom.com',
    'Origin': 'http://sz.ziroom.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://sz.ziroom.com/ditu/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv 11.0) like Gecko',
    'X-Requested-With': 'XMLHttpRequest',
}

data={
   'dn':'',
   'bn':'',
   'slc':'',
   'ssc':'',
   'p':'1',
}

ret=requests.post(url,headers=headers,data=data).text
ret=json.loads(ret)
room_list=ret['list']
print(len(room_list))
print(ret['count'])
print(ret)

print('sz',5711)




