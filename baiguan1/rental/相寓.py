# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


# url='http://gj2.1zu.com/api/houseListJsonp?callback=successCallback&pageNum=2&_=1510022016448'
#
# headers={
# 	'Host': 'gj2.1zu.com',
# 	'Referer': 'http://m.1zu.com:8080/views/houseSourceList.html',
# 	'Accept-Encoding': 'gzip, deflate',
# 	'Accept': '*/*',
# 	'Cookie': 'JSESSIONID=E6188D8CD61FCA51546DA7C6FB52812E',
# 	'Accept-Language': 'zh-cn',
# 	'Connection': 'keep-alive',
# 	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/zh_CN',
# }

url='http://m.5i5j.com/sh/rent/getlist?page=2&pathInfo=x1'
headers={
'Host'	:'m.5i5j.com',
'Referer':	'http://m.5i5j.com/sh/rent/x1',
'X-Requested-With':	'XMLHttpRequest',
'Accept-Encoding':	'gzip, deflate',
'Accept'	:'text/html, */*; q=0.01',
'Accept-Language'	:'zh-cn',
'Cookie'	:'PHPSESSID=atrs2jomt8ll93s84usjv9rfu1; _ga=GA1.2.782634927.1510021695; _gat=1; _gid=GA1.2.2047064868.1510021695; _va_id=36651db0b3ca387e.1510021692.1.1510021762.1510021692.; _va_ses=*; yfx_c_g_u_id_10000001=_ck17110710280615660605767063492; yfx_f_l_v_t_10000001=f_t_1510021686541__r_t_1510021686541__v_t_1510021686541__r_c_0',
'Connection'	:'keep-alive',
'User-Agent'	:'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/zh_CN',
}
ret=requests.get(url,headers=headers).content.decode()
print(ret)

