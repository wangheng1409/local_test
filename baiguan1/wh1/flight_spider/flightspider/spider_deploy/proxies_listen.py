#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flightspider import database
from flightspider import settings
import requests
import time
import json


limit=20
while True:
    remotid_list=database.db.query("SELECT remoteID FROM http_proxy WHERE state = 4")
    remotid_list=list(set(map(lambda x:int(x.values()[0]),remotid_list)))
    print remotid_list
    #拉黑或重播ip
    for item_id in remotid_list:
        url='http://%s/api/v2/ip/%s'%(settings.HTTP_PROXY_HOST,item_id)
        data={
            'action':'blacklist',
            'disable_time':'24h'
        }
        requests.post(url=url,data=data)
    #拨号完成状态置为禁用
    database.db.update("UPDATE http_proxy SET state=%s WHERE state=%s " % (3, 4))
    #获取新ip,并写入数据库
    if remotid_list:
        time.sleep(10)
    url = "http://%s/api/v2/ip?scenes=air_spider_xz&limit=%s" % (settings.HTTP_PROXY_HOST, limit)
    rep = requests.get(url)
    obj = json.loads(rep.text)
    if obj.get("data", None):
        ip_list = obj["data"]["ip_list"]
        print "Success request %d IP" % len(ip_list)
        print ip_list
        for item in ip_list:
            print type(item)
            database.db.update("UPDATE http_proxy SET state=%s WHERE remoteID=%s " % (3, item["id"]))
            database.insert_http_prxoy(item["id"], item["proxies"])
    else:
        print obj.get('error').get('message')




