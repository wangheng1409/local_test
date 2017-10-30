import requests
import json
import random


class_id='VCZ4870'
commonStudentInfoList=[

    {"id":-1,"isDelete":False,"webAccountCode":"160308104604921_v","bOldStudent":False,"studentCode":"","name":"王"+str(a),"gender":"1",
     "mobile":"186"+''.join([str(random.randint(0,9)) for i in range(8)]),"phoneHead":"","phoneBody":"","phoneFoot":"","districtCode":"","idCard":"123456","increment":"","certNum":"",
     "nCertificateType":"2","sGradeValue":"155","sGradeText":"1年级"} for a in range(9) ]

stuSheetInfoList=[

    {"guid":"guid_"+str(a+1),"name":'王'+str(a),"studentCode":"","sex":"1","mobile":"186"+''.join([str(random.randint(0,9)) for j in range(8)]),"phoneHead":"","phoneBody":"","phoneFoot":"",
     "districtCode":"","idCard":"123456","increment":"","certNum":"","nCertificateType":"2","sGradeValue":"155","sGradeText":"1年级"}  for a in range(9) ]

studentClassInfoList=[{"guid":"guid_" +str(a+1),"tag":"王"+str(a),"classCode":class_id,"studentCode":"","isRecommendPeople":False} for a in range(9)
                  ]

wayList=[{"id":4,"isReceiveOwn":True,"name":"自取","fees":0,"remark":"","checked":True,"provinces":None,"citys":None,"districts":None}]
data={
    'schoolId'	:2,
    'commonStudentInfoList'	:json.dumps(commonStudentInfoList),
    'stuSheetInfoList':	json.dumps(stuSheetInfoList),
    'studentClassInfoList':	json.dumps(studentClassInfoList),
    'wayList'	:json.dumps(wayList),
    'voucherUseList':json.dumps([]),
    'addressInfoList':json.dumps([]),
    'stuSeatInfoList':json.dumps([]),
    'studentCardInfoList':json.dumps([]),
}

url='http://baoming.xdf.cn/ShoppingCart/Handlers/addOrderHandler.ashx'

# header={
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Cookie': 'Fingerprint_xdf=6a9210503a9d66dcf8733672496f2a51; __xfid=1497937938635_452377; '
#               'soukecityid=1; U2Token=D92BEFFE71CAF140F4EF5C76974F6A0D_2B125CC2E062C9B74FC68EA1ED65B665;'
#               ' U2User=W2Vh%2Bf3P%2FAoJfXMzuQVIMw%3D%3D; U2NickName=170626110526050_v; ASP.NET_SessionId=oyp3z2daszldor5r3haiyogc;'
#               ' baoming_cookie=R0018201412; Xdf.MarketingSources=MSouke; IsCheckLogin=0; IsShowPay=0; '
#               'AppId=MSouke; U2Last=baoming.xdf.cn; soukeClassHistory=1-SAC1775%2C1-SAC17100%2C1-'+class_id+'%2C1-SA171324C;'
#               ' __utmt=1; __utmt_t3=1; Xdf.WebPay.V4.LimitClasses=; Xdf.WebPay.V5.historyCart=; '
#               'Xdf.WebPay.V4.Cart='+class_id+'%2C%25E4%25B8%2580%25E5%25B9%25B4%25E7%25BA%25A7%25E8%258B%25B1%25E8%25AF%25AD%25E5%25B0%2596%25E5%25AD%2590%25E7%25A7%258B%25E5%25AD%25A3%25E7%258F%25AD%2C1%2C%25E5%258C%2597%25E4%25BA%25AC%25E6%2596%25B0%25E4%25B8%259C%25E6%2596%25B9%2C3580%2C%2C5; Xdf.WebPay.V4.Store=; bankOfChinaCart=; __utma=1.552946271.1497264560.1498444227.1498447399.18; __utmb=1.12.9.1498452014825; __utmc=1; __utmz=1.1497937939.13.2.utmcsr=souke.xdf.cn|utmccn=(referral)|utmcmd=referral|utmcct=/Course/46-46-10791.html; __utmv=1.|2=status=newer=1',
#     'Host': 'baoming.xdf.cn',
#     'Origin': 'http://baoming.xdf.cn',
#     'Proxy-Connection': 'keep-alive',
#     'Referer': 'http://baoming.xdf.cn/ShoppingCart/ordertofillin.html?mode=default',
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest'
# }

header={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'Fingerprint_xdf=6a9210503a9d66dcf8733672496f2a51; __xfid=1497937938635_452377;'
              ' U2Token=D92BEFFE71CAF140F4EF5C76974F6A0D_2B125CC2E062C9B74FC68EA1ED65B665;'
              ' U2User=W2Vh%2Bf3P%2FAoJfXMzuQVIMw%3D%3D; U2NickName=170626110526050_v; '
              'ASP.NET_SessionId=oyp3z2daszldor5r3haiyogc; Xdf.MarketingSources=MSouke; '
              'IsCheckLogin=0; IsShowPay=0; AppId=MSouke; U2Last=baoming.xdf.cn; baoming_cookie=R0018202529; '
              'soukecityid=2; Hm_lvt_19fadb255d5df879f17dc1cfb7d9969d=1498458636; '
              'Hm_lpvt_19fadb255d5df879f17dc1cfb7d9969d=1498458636; '
              'soukeClassHistory=2-YW1DM01N%2C1-SAY17725%2C1-SAY17651%2C2-'+class_id+'; __utmt=1;' 
               ' __utmt_t3=1; Xdf.WebPay.V4.LimitClasses=; Xdf.WebPay.V5.historyCart=; '
               'Xdf.WebPay.V4.Cart='+class_id+'%2C%25E5%2588%259D%25E4%25B8%2580%25E6%258F%2590%25E9%25AB%2598%25E8%258B%25B1%25E8%25AF%25AD%25E6%259A%2591%25E5%2581%2587%25E7%258F%25AD%25EF%25BC%25886%25E4%25BA%25BA%255B%2524%255D%25E8%25B5%25B0%25E8%25AF%25BB%25EF%25BC%2589%2C2%2C%25E4%25B8%258A%25E6%25B5%25B7%2C3720%2C%25E6%25AD%25A3%25E5%25B8%25B8%25E6%258A%25A5%25E5%2590%258D%2C10;'
               ' Xdf.WebPay.V4.Store=; bankOfChinaCart=; __utma=1.552946271.1497264560.1498447399.1498455955.19; __utmb=1.189.9.1498460882824;'
                ' __utmc=1; __utmz=1.1497937939.13.2.utmcsr=souke.xdf.cn|utmccn=(referral)|utmcmd=referral|utmcct=/Course/46-46-10791.html; __utmv=1.|2=status=newer=1',
    'Host': 'baoming.xdf.cn',
    'Origin': 'http://baoming.xdf.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://baoming.xdf.cn/ShoppingCart/ordertofillin.html?mode=default',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
ret=requests.post(url=url,data=data,verify=False,headers=header)
print(ret.text)