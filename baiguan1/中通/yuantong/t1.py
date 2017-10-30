# !/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import time
data={
    'waybillNo':'885686205649860945/886216399422476138',
    'validateCode':'',
    'jsessionId':'',
}

url='http://trace.yto.net.cn:8022/TraceSimple.aspx'

headers={
    'Host': 'trace.yto.net.cn:8022',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://www.yto.net.cn',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://www.yto.net.cn/gw/index/index.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': 'ASP.NET_SessionId=lzgkwiq4h3dpg1l53cxyvyde',
}

ret=requests.post(url=url,data=data,headers=headers,verify=False).text
print(ret)