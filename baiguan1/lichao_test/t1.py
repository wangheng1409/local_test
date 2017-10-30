import requests
import random
import time
import json
from lichao_test import pytesseract
from PIL import Image

session=requests.session()
headers0={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'aso100.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
}
ret=session.get('https://aso100.com/',verify=False)

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '61',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'aso100.com',
    'Origin': 'https://aso100.com',
    'Referer': 'https://aso100.com/account/signin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
ret1='未识别出，请重新设置参数'
while True:
    f=open('a.png','wb')
    f.write(session.get('https://aso100.com/account/getVerifyCodeImage?1497428845914',verify=False).content)
    f.close()
    pil_im=Image.open('a.png').convert('L')
    pil_im.show()
    time.sleep(2)
    def initTable(threshold=100):
         table = []
         for i in range(256):
             if i < threshold:
                 table.append(0)
             else:
                 table.append(1)

         return table
    binaryImage = pil_im.point(initTable(), '1')
    binaryImage.show()
    vcode = pytesseract.image_to_string(binaryImage)

    print (vcode)

    data={
        'username':15210617990,
        'password':'naruto1b',
        # 'code':input('code'),
        'code':vcode,
        'remember':True
    }

    ret1=session.post('https://aso100.com/account/signinForm',headers=headers,data = data).content.decode('utf-8')
    print(ret1)
    if json.loads(ret1)['code']==10000:
        break
print(ret1)