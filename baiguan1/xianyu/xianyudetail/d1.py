import grequests
import requests
from bo_lib.general import ProxyManager
from concurrent import futures
import time
import redis
import json
import random
from lxml import etree
# from gevent import monkey; monkey.patch_all()
import gevent
from lxml import etree
import re
import gc
import pymongo
from concurrent.futures import ThreadPoolExecutor, as_completed
from pympler import summary
from pympler import muppy
from scrapy.http import TextResponse

client=pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
db=client.xianyu.detail



start=time.time()
pm = ProxyManager()
TEST=True
redis_key = 'xianyu_item_10000'

def random_t(l):
    return ''.join(
        map(lambda i: chr(random.randint(97, 122)) if random.randint(1, 4) in [1, 2] else str(random.randint(0, 9)),
            range(l)))

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
urls=[]
for data in data_list:
    item_id = json.loads(data.decode(), encoding='utf-8')
    ur = 'https://2.taobao.com/item.htm?id='+str(item_id)
    urls.append(ur)

slice_list=[] #切成功后的 ：[[],[],[],[]]
_slice=10
for i in range(len(urls)//_slice):
    a=urls[:_slice]
    del urls[:_slice]
    slice_list.append(a)
ll=len(slice_list)*_slice
print('slice_list ok',ll)
print(slice_list)
client = pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
db = client.xianyu.item_detail

class XianyuSpider():

    def __init__(self,url_item):
        self.urls = []
        self.finish_url_num = 0
        self.insert_list = []
        self.work(url_item)


    def work(self,slice_item):
        ret=(grequests.get(u, headers=headers, proxies=pm.getProxyV2(),timeout=20,data={'ur':u}) for u in slice_item)
        ret=grequests.imap(ret,size=100)
        print(ret)
        for i in ret:
            # while 'login' in i.url:
                # i = requests.get(i.data['ur'], headers=headers, proxies=pm.getProxyV2(), timeout=20,data={'ur':i.data['ur']})
            i = TextResponse(url=i.url, body=i.content)

            self.finish_url_num+=1
            print(123,self.finish_url_num)
            s = {}
            print(i.url)
            s['item_id'] = re.findall('id=(\d+)', i.url)[0]
            s['editor_time'] = \
            i.xpath('//div[@id="idle-detail"]//div[@class="others-wrap"]/ul//li[2]//span/text()').extract()[0]
            s['user_id'] = i.xpath('//div[@class="wangwang"]/a/text()').extract()[0]
            s['item_name'] = i.xpath('//div[@id="J_Property"]//h1/text()').extract()[0]
            s['price'] = i.xpath('//div[@id="J_Property"]//li[@class="price-block"]//em/text()').extract()[0]
            s['salse_status'] = 1 if "已经售出" in i.text else 0
            self.insert_list.append(s)
            if len(self.insert_list) == 10:
                db.insert_many(self.insert_list)
                self.insert_list = []
                print('+++++++++++')
            print(s)


def gen_executor(work, slice_list):
    workers = 10
    with ThreadPoolExecutor(workers) as executor:
        futures = [executor.submit(work, slice_item) for slice_item in slice_list]
        for future in as_completed(futures):
            futures.remove(future)
            yield

for cycle in gen_executor(XianyuSpider, slice_list):
    gc.collect()
    summary.print_(summary.summarize(muppy.get_objects()), limit=4)

print(time.time()-start)
