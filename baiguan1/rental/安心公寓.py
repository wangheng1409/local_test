# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='https://www.axhome.com.cn/ajax/storeList.html?city_id=76&district_id=0&metro=&trading_area=&keyword=&delete_store_id=&p=1'


headers={
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'SERVERID=8aa51ed7e1375fa7592347ad12b4e65a|1509601535|1509601535; Hm_lvt_b9d12d93a830f7244fd428268ec7f6c6=1509601536; Hm_lpvt_b9d12d93a830f7244fd428268ec7f6c6=1509601536',
    'Host':'www.axhome.com.cn',
    'Referer':'https://www.axhome.com.cn/storeList.html?city_id=76&city_name=%E5%B9%BF%E5%B7%9E',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
}

ret=requests.get(url,headers=headers,verify=False).text
print(ret)

