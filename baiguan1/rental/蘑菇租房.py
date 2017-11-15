# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://sz.mogoroom.com/list'

headers={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'JSESSIONID=FF6FCA4AF8C8F5BF40F05635470BEF18-n2; gr_user_id=3564ba29-565a-420a-9548-d259376e4a46; bad_id9d030e80-e73e-11e5-b771-11c8f335ec09=c8ff7141-bf8c-11e7-bd1b-4dbaaa471b55; nice_id9d030e80-e73e-11e5-b771-11c8f335ec09=c8ff7142-bf8c-11e7-bd1b-4dbaaa471b55; hadoop_renter_key=62022a0f-6928-4519-a0be-fb25b680f534; gr_session_id_aca7dc2ea0f02f49=8c2f777d-09bc-4a91-bd22-195d0f5eecf9; JSESSIONID=FF6FCA4AF8C8F5BF40F05635470BEF18-n2',
    'Host': 'sz.mogoroom.com',
    'Origin': 'http://sz.mogoroom.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://sz.mogoroom.com/list?page=2',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

data={
    'page':'1'
}

ret=requests.post(url,headers=headers,data=data).text
print(ret)





