# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://www.qk365.com/list/p2'

headers={
    'Host': 'www.qk365.com',
    'Cache-Control'	:'max - age = 0',
    'Origin': 'http://www.qk365.com',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://www.qk365.com/list',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    # 'Cookie': 'SESSION=d4c1c4c2-b53a-4b8a-839b-58b40dc79e08; topShowTag=hide; JSESSIONID=859933794BBDF022631A04D5EA052B81; visitorId=7C4F336C-6E0C-45DC-9163-AFB2AE775E1F; gr_user_id=7deb211d-c158-42ba-8a00-8f3445877ebc; _gat=1; sourceMark=lisft; Hm_lvt_53c8bf761df44282a0cf7d4949581592=1509598254; Hm_lpvt_53c8bf761df44282a0cf7d4949581592=1509599129; gr_session_id_9553c2fcfe1abe89=2c06c36b-7324-4739-bbf7-9214bc4c4d8a; _ga=GA1.2.434532609.1509598256; _gid=GA1.2.401923633.1509598256; cs=2; nb-referrer-hostname=www.qk365.com; nb-start-page-url=http%3A%2F%2Fwww.qk365.com%2Flist',
}

ret=requests.get(url,headers=headers).text
print(ret)



