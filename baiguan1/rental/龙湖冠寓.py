# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://guanyu.longfor.com/html/h5/index.html'

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Host': 'guanyu.longfor.com',
    'If-Modified-Since': 'Thu, 26 Oct 2017 11:57:34 GMT',
    'If-None-Match': 'W/"59f1cdae-2eab"',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

# ret=requests.get(url,headers=headers).content.decode()
# print(ret)

url2='http://guanyu.longfor.com/html/h5/detailPagetyyxy.html'
hed={
'Host':'guanyu.longfor.com',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8',
}
ret=requests.get(url2,headers=hed).content.decode()
print(ret)