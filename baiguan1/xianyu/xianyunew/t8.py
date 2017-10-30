import grequests
import requests
from bo_lib.general import ProxyManager
from concurrent import futures
import time
import redis
import json
# from gevent import monkey; monkey.patch_all()
import gevent
import sys
index=sys.argv[1]

start=time.time()
pm = ProxyManager()
TEST=False
redis_key = 'two_xianyuspider_redis'

headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'cache-control':'max-age=0',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
}

if not TEST:
    pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
else:
    pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
r = redis.Redis(connection_pool=pool)
print(type(index))
data_list=r.lrange(redis_key,index,int(index)+2)
print(data_list)
urls=[]
for data in data_list:
    store_item = json.loads(data.decode(), encoding='utf-8')
    category_name = store_item['category_name']
    catid = store_item['catid']
    page = store_item['page']
    referer = store_item['referer']
    headers.update({'referer':referer})
    t = str(time.time()).replace('.', '')
    ur = 'https://s.2.taobao.com/list/waterfall/waterfall.htm?' \
        'wp=' + str(page) + '&' \
        '_ksTS=' + t[:-3] + '_' + t[-3:] + '&' \
        'callback=jsonp114&' \
        'stype=1&' \
        'catid=' + str(catid) + '&' \
        'st_trust=1&ist=1'
    while True:
        ret=requests.get(ur, headers=headers, proxies=pm.getProxyV2(),timeout=10).text
        left = ret.index('{')
        try:
            dic = json.loads(ret[left:].strip()[:-1].replace('\\', '/'))
        except Exception as e:
            print(e, 'json error', ret)
            dic = json.loads(ret[left:].strip()[:-1].replace('\\', '/'))
            print('ok')
        try:
            all_page=dic['totalPage']
        except:
            all_page=-1
        if all_page!=-1:
            break
        time.sleep(1)
    print(category_name,all_page)
    for i in range(all_page):
        ur = 'https://s.2.taobao.com/list/waterfall/waterfall.htm?' \
            'wp=' + str(i) + '&' \
            '_ksTS=' + t[:-3] + '_' + t[-3:] + '&' \
            'callback=jsonp114&' \
            'stype=1&' \
            'catid=' + str(catid) + '&' \
            'st_trust=1&ist=1'
        urls.append(ur)



slice_list=[] #切成功后的 ：[[],[],[],[]]
_slice=1000
for i in range(len(urls)//_slice):
    a=urls[:_slice]
    del urls[:_slice]
    slice_list.append(a)
ll=len(slice_list)*1000
print('slice_list ok',ll)

j=0
def work(slice_item):
    global j
    ret=(grequests.get(u, headers=headers, proxies=pm.getProxyV2(),timeout=10) for u in slice_item)
    ret=grequests.imap(ret,size=100)
    for i in ret:
        if 'numFound' in i.text:
            j+=1
            print(j,j/ll,'='*20)
            if i%100==0:
                print(time.time() - start)
        else:
            print(i)
            print(i.url)

workers=10
with futures.ThreadPoolExecutor(workers) as executor:
    res=executor.map(work,slice_list)
print(1000,j)
print(time.time()-start)
