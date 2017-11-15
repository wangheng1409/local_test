# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://www.homeplus.cn/zj/index_2.jhtml?city=%E5%B9%BF%E5%B7%9E&cityCode=440100'

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Cookie': 'SESSION=aa738db8121d4e36b5af5704e48bb980; _site_id_cookie=1; _cookie_city_name=%E5%B9%BF%E5%B7%9E; clientlanguage=zh_CN',
    'Host': 'www.homeplus.cn',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

ret=requests.get(url,headers=headers).text
print(ret)

