import requests
import base64
url='https://s.2.taobao.com/list/waterfall/waterfall.htm?wp=2&_ksTS=1502424139973_130&callback=jsonp131&stype=1&catid=50100399&st_trust=1&ist=1'

proxyServer = "http://proxy.abuyun.com:9020"
proxyUser = "H90C6N3NH81A1R6D"
proxyPass = "1869CE18BD98C84E"
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
header={
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'cache-control':'max-age=0',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    "Proxy-Authorization":proxyAuth
}

proxie = {
        'http' : proxyServer
    }
j=0
total=1000
for i in range(total):
    ret=requests.get(url=url,headers=header,verify=False,proxies=proxie).text
    if 'numFound' in ret:
        print('ok')
    else:
        j+=1
        print(ret)
print(total,j)
