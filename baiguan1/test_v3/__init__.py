# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

proxies = {
    "http": "http://222.94.147.224:15037",
}

ret=requests.get('https://www.kuaidi100.com/query?type=shentong&postid=8721224802562&id=1&valicode=&temp=0.9787904922508787',
                 proxies=proxies).text
print(ret)
