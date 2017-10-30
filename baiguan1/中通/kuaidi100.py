import random
import requests
s='0.'+str(random.choice([x for x in range(1,10)]))+''.join([str(random.choice([x for x in range(10)])) for i in range(15)])
url='https://www.kuaidi100.com/query?type=jd&postid='+'60066247971'+'&id=1&valicode=&temp='+s
# url='https://www.kuaidi100.com/query?type=jd&postid=60066247971&id=1&valicode=&temp=0.6056862525692348'
head={
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Host':'www.kuaidi100.com',
'Referer':'https://www.kuaidi100.com/all/jd.shtml',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',
}
print(requests.get(url,headers=head).text)