# !/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
import json
import grequests
import requests
import re
import random
import time
import copy
import requests.adapters
from requests.adapters import HTTPAdapter
from bo_lib.general import ProxyManager
from scrapy.http import TextResponse
pm = ProxyManager()


start=time.time()
requests.adapters.DEFAULT_RETRIES = 5
def random_t(l):
    return ''.join(
        map(lambda i: chr(random.randint(97, 122)) if random.randint(1, 4) in [1, 2] else str(random.randint(0, 9)),
            range(l)))

redis_key = 'xianyu_item_10000'
TEST=True
headers = {
'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.8',
'cache-control':'max-age=0',
'cookie':'v=0; cookie2='+random_t(32)+'; t='+random_t(32)+'; _tb_token_=ea493e35e5b3b; cna=7UIUEr29+A0CAXaQhSXRK9Rc; isg=Anh4l7YaVWwONbnMjEC0UmmZSSDKSc8CMU_csLLplrNtzRm3WvAj-y0t8_MG',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
}
if not TEST:
    pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
else:
    pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
r = redis.Redis(connection_pool=pool)

data_list=r.lrange(redis_key,0,-1)
for data in data_list:
    r.lpush(redis_key+'tmp',data)
while r.exists(redis_key+'tmp'):
    item_id = json.loads(r.rpop(redis_key+'tmp').decode(), encoding='utf-8')
    ur = 'https://2.taobao.com/item.htm?id='+str(item_id)+'&from=list&similarUrl='
    session = requests.session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    i=session.get(ur, headers=headers, proxies=pm.getProxyV2(),timeout=20)
    i.keep_alive = False
    j = copy.deepcopy(i)
    if i.status_code==404:
        continue

    try:
        print(i, i.status_code)
        i=TextResponse(url=i.url,body=i.content)
        print(123)
        s = {}
        print(i.url)
        s['item_id'] = re.findall('id=(\d+)', i.url)[0]
        s['editor_time'] = i.xpath('//div[@id="idle-detail"]//div[@class="others-wrap"]/ul//li[2]//span/text()').extract()[0]
        s['user_id'] = i.xpath('//div[@class="wangwang"]/a/text()').extract()[0]
        s['item_name'] = i.xpath('//div[@id="J_Property"]//h1/text()').extract()[0]
        s['price'] = i.xpath('//div[@id="J_Property"]//li[@class="price-block"]//em/text()').extract()[0]
        s['salse_status'] = 1 if "已经售出" in i.text else 0
        print(s)
    except:
        ur=[x.url for x in j.history][0]
        print('retry_url',ur)
        item_id_retry=re.findall('id=(\d+)', ur)[0]
        r.lpush(redis_key + 'tmp', json.dumps(str(item_id_retry)))
        time.sleep(3)


print(time.time()-start)

