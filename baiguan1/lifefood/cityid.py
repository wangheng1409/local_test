# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time
import re

cities_dic = {
    'beijing': '北京',
    'shanghai': '上海',
    'suzhou': '苏州',
    'ningbo': '宁波',
    'nanjing': '南京',
    'guangzhou': '广州',
    'wuhan': '武汉',
    'xian': '西安',
    'huaian':'淮安',
    'hangzhou': '杭州',
    'nanning': '南宁',
    'kunming': '昆明',
    'chongqing': '重庆',
    'chengdu': '成都',
    'dalian': '大连',
    'changchun': '长春',
    'yangzhou': '扬州',
    'changzhou': '常州',
    'wuxi': '无锡',
    'taizhou': '泰州',
    'hefei': '合肥',
    'jiaxing': '嘉兴',
    'nanchang': '南昌',
    'nantong': '南通',
    'zhenjiang': '镇江',
    'zhangjiagang':'张家港',
    'jiangyin':'江阴',
    'shenzhen': '深圳',
    'dongguan': '东莞',
    'taiyuan': '太原',
    'tianjin': '天津',
    'guiyang': '贵阳',
    'shijiazhuang': '石家庄',
}
s={}
base_url='http://www.dianping.com/{}'
for city in cities_dic:
    url=base_url.format(city)
    print(url)
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Cookie':'_lxsdk_s=%7C%7C0',
        'Host':'www.dianping.com',
        'Proxy-Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    }
#
    ret=requests.get(url,headers=headers).text
    cityId=re.findall("'cityId': '(\d+)'",ret)[0]
    s[city]=cityId
    print(s)
