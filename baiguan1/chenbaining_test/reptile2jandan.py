#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request as re
import time

# 定义元素
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0"
url = 'http://jandan.net/ooxx/page-399#comments'
accept = '*/*'
accept_encoding = 'gzip, deflate'
accept_language = 'zh-CN,zh;q=0.9'
connection = 'keep-alive'
host = 'jandan.net'

headers = {'User-Agent': user_agent, 'Accept': accept, 'Accept-Encoding': accept_encoding,
           'Accept-Language': accept_language, 'Connection': connection, 'Host': host}

# 输入地址得到request
req = re.Request(url, headers=headers)

# 然后执行请求
respone = re.urlopen(url)

# 根据respone得到页面
html = respone.read().decode('utf-8')
# 打印
print(html)
