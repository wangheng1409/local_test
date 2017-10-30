import requests
import time
import json
print(time.time())
ids='719587492915'
url='https://sp0.baidu.com/9_Q4sjW91Qh3otqbppnN2DJv/pae/channel/data/asyncqury?' \
    'cb=jQuery110205330766960218309_1500280361027' \
    '&appid=4001' \
    '&com=zhongtong' \
    '&nu='+ids+'&vcode=' \
    '&token=&_='+str(time.time()).replace('.','')[:13]

head={
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Cookie':'BAIDUID=0097B38CA9D585AF11219CE0CED3C64D:FG=1; cart_id=261882836; BIDUPSID=0097B38CA9D585AF11219CE0CED3C64D; PSTM=1500280360; PSINO=1; H_PS_PSSID=1461_21078_20930',
'Host':'sp0.baidu.com',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',

}

ret=requests.get(url,headers=head)
# print(ret.text[ret.text.index('{'):-1])
print(json.loads(ret.text[ret.text.index('{'):-1]))