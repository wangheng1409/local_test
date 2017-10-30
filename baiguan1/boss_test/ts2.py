
import requests
from lxml import html
import json
import time
def headers(page,city,keywords):
    url='https://www.zhipin.com/boss/search/geeks.json?' \
        'page='+str(page)+ \
        '&jobId=' \
        '&jobs=' \
        '&companies=' \
        '&skills=' \
        '&schools=' \
        '&keywords='+keywords+ \
        '&city='+str(city)+ \
        '&_='+str(time.time()).replace('.','')[:13]

    head={
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'www.zhipin.com',
        'Cookie': '__c=1499399875; __g=-; lastCity=101010100; JSESSIONID=""; t=lGfv4ZXN9hMtm4ks; wt=lGfv4ZXN9hMtm4ks; __l=r=&l=%2Fc101010100-p170101%2Fs_301-y_2-t_801%2F%3Fpage%3D2%26ka%3Dpage-2; __a=36808995.1499399875..1499399875.25.1.25.25; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1499399876; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1499664630',
        'Referer':'https://www.zhipin.com/boss/search/geek.html',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
    }
    return url,head
if __name__ =='__main__':

    url,head=headers(1,101010100,'python')
    print(url)
    res=requests.get(url=url,headers=head,verify=False)

    res_dict=json.loads(res.content.decode())
    print(res_dict)
    s=res_dict['htmlList'].replace('\n','')
    response=html.fromstring(s)
    ele_info_list = response.xpath('//li/a/@href')[0]
    print(ele_info_list)