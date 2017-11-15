# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://www.meyouhome.cn/operation/huntHouse_list?type=huntHouse_list&pageIndex=16'

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': 'ASP.NET_SessionId=nc1ampytveswey4q4qet0ci3; Hm_lvt_21b748150f05e3c0d61307def0e638ba=1509603374; Hm_lpvt_21b748150f05e3c0d61307def0e638ba=1509603379',
    'Host': 'www.meyouhome.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.meyouhome.cn/operation/huntHouse_list?type=huntHouse_list',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

ret=requests.get(url,headers=headers,verify=False).text
print(ret)

