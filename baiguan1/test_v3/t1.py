# !/usr/bin/env python
# -*- coding:utf-8 -*-

# from bo_lib.general.proxy_manager import ProxyManagerV2
# from tenacity import retry
#
#
# @retry
# def run():
#     ProxyManagerV2().start()
#
# run()
import requests
import time

class ProxyManagerV2(object):
    def __init__(self):
        self.url = 'http://dynamic.goubanjia.com/dynamic/get/90fed17ad6aada3dfbe0237b26c77d9c.html?random=yes'
        self.client = RedisHelper().client

    def start(self):
        while True:
            proxy_list = requests.get(self.url).text.split('\n')
            for proxy in proxy_list:
                if not proxy:
                    continue
                # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), proxy)
                self.client.rpush('proxy', 'http://{}'.format(proxy.strip()))
                if self.client.llen('proxy') > 5:
                    self.client.lpop('proxy')
                time.sleep(0.1)



ProxyManagerV2().start()

