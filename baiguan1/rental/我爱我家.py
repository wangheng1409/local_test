# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://bj.5i5j.com/rent/n101'

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Host': 'bj.5i5j.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://bj.5i5j.com/rent/n100',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',}

ret=requests.get(url,headers=headers).content.decode()
print(ret)

import random
print(random.random())

