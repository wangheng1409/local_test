# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://www.ziroom.com/map/room/list?' \
    'min_lng=116.132352&' \
    'max_lng=116.675648&' \
    'min_lat=39.775842&' \
    'max_lat=40.053874&' \
    'clng=116.404&' \
    'clat=39.915&' \
    'zoom=12&' \
    'p=10'

headers={
    'Host': 'www.ziroom.com',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Referer': 'http://www.ziroom.com/map/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    # 'Cookie': 'PHPSESSID=frcrcm78c8ileitavphfp42bt5; gr_user_id=fad7c88e-540e-4758-b51c-8008893dbb75; hlwyfb_m_current_city_code=110000; aliyungf_tc=AQAAANV9aRQ6ugUAKoRFeT4HWnROH4RT; CURRENT_CITY_NAME=%E5%8C%97%E4%BA%AC; mapType=%20; gr_session_id_8da2730aaedd7628=435dee62-a2d6-4824-b6b8-823ad9264d85; CURRENT_CITY_CODE=110000',
}

ret=requests.get(url,headers=headers).text
print(ret)

