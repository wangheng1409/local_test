from lxml import etree
import requests
header={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Host':'www.stats.gov.cn',
    'If-Modified-Since':'Mon, 22 May 2017 00:44:43 GMT',
    'If-None-Match':'"b054a-550122d52ab3b-gzip"',
    'Proxy-Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
}
ret=requests.get('http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201703/t20170310_1471429.html',headers=header).content.decode()
print(ret)
