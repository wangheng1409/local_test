import time
start=time.time()
import grequests
from bo_lib.general import ProxyManager
url='https://s.2.taobao.com/list/waterfall/waterfall.htm?wp=2&_ksTS=1502424139973_130&callback=jsonp131&stype=1&catid=50100399&st_trust=1&ist=1'
urls=[url]*1000
headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'cache-control':'max-age=0',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
}
pm = ProxyManager()

j=0
ret=(grequests.get(u, headers=headers, proxies=pm.getProxyV2()) for u in urls)
ret=grequests.imap(ret,size=30)
for i in ret:
    if 'numFound' in i.text:
        print('ok')
    else:
        j+=1
        print(i)
print(1000,j)
print(time.time()-start)
