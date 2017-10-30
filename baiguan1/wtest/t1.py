import requests

h={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Cookie':'_gscu_273633028=9563012136igxd18; _gscbrs_273633028=1; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1495630121; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1495893023',
'Host':'www.ccgp.gov.cn',
'Proxy-Connection':'keep-alive',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
r=requests.get('http://www.ccgp.gov.cn/cggg/dfgg/zbgg/201705/t20170527_8308131.htm',headers=h).content
print(r.decode('utf8'))
