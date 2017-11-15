# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://www.yujiangongyu.com/ofcFront/search/list'

headers={
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'LXB_REFER=www.google.com; Hm_lvt_f8b3b77cf74d24c53f94e207ca2bfffb=1509604094; Hm_lpvt_f8b3b77cf74d24c53f94e207ca2bfffb=1509604396; nb-referrer-hostname=www.yujiangongyu.com; nb-start-page-url=http%3A%2F%2Fwww.yujiangongyu.com%2Fditu; JSESSIONID=260C0ED04ABC900F806A4B5AC6B9F92E',
    'Host': 'www.yujiangongyu.com',
    'Origin': 'http://www.yujiangongyu.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.yujiangongyu.com/ditu',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

data={
    'bizAreaId':'1001154',
    'communityId':'',
    'page':'5',
}

ret=requests.post(url,headers=headers,data=data).text
print(ret)





