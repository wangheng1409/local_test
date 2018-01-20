# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time

keyword='赛百味'
page=1
base_url='http://www.dianping.com/search/keyword/2/0_{}/p{}'
url=base_url.format(keyword,str(page))
print(url)

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Cookie':'_lxsdk_s=%7C%7C0',
    'Host':'www.dianping.com',
    'Proxy-Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}
#
ret=requests.get(url,headers=headers).text
print(ret)

