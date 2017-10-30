import requests
import time
import json
ty_id='78925'
ty_name='短袖T恤'
page=2
ur='https://m.vip.com/server.html?rpc&method=getClassifyList&f=&_='+str(time.time()).replace('.','')[:-3]
data={
    "method": "getClassifyList",
    "params": {
        "page": "classify-list-"+str(ty_id)+"-0-0-0-0-1-20.html",
        "np": page,
        "ep": 20,
        "category_id": "",
        "brand_store_sn": "",
        "filter": "",
        "sort": "0",
        "minPrice": "",
        "maxPrice": "",
        "query": "title="+'%E7%9F%AD%E8%A2%96T%E6%81%A4'
    },
    "id": int(str(time.time()).replace('.','')[:-3]),
    "jsonrpc": "2.0"
}

head={
    'Host'	:'m.vip.com',
    'Connection':	'keep-alive',
    # 'Content-Length':'270',
    'Origin'	:'https://m.vip.com',
    'User-Agent'	:'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
    'Content-Type'	:'application/json',
    'Accept'	:'application/json',
    'X-Requested-With':	'XMLHttpRequest',
    'Accept-Encoding':	'gzip, deflate, br',
    # 'Origin-Referer':'https://m.vip.com/classify-list-78925-0-0-0-0-1-20.html?title=%E7%9F%AD%E8%A2%96T%E6%81%A4',
    # 'Referer':'https://m.vip.com/classify-list-78925-0-0-0-0-1-20.html?title=%E7%9F%AD%E8%A2%96T%E6%81%A4',
    'Accept-Language':	'zh-CN,zh;q=0.8',
    'Cookie'	:'WAP_ID=6d653eb613f43d95b122061474cbbb56d8b162d3;'
                 # ' WAP[locateip]=2034598954%2C101101%2CVIP_BJ%2C;'
                 ' WAP[oxo_area]=101101%2C101101101%2C; '
                 '_smt_uid=5965ceb0.a4ccffc;'
                 ' WAP[%2Findex.html]=1; '
                 'source=www;'
                 ' WAP[back_act]=%2Fproduct-1291007-208970514.html;' #可变
                 ' provinceId=104104; '
                 'wap_A1_sign=1; '
                 'appCommonParam=%7B%7D; '
                 'WAP[p_area]=%25E5%258C%2597%25E4%25BA%25AC;'
                 ' WEIXIN_PROVINCE=%E5%8C%97%E4%BA%AC; '
                 'm_vip_province=101101; '
                 'WEIXIN_PROVINCEID=101101;'
                 ' WAP[p_wh]=VIP_BJ; '
                 'warehouse=VIP_BJ; '
                 'WEIXIN_WAREHOUSE=VIP_BJ;'
                 ' mar_ref=classify;'
                 ' mars_pid=57; '#可变
                 'mars_cid=1499847024497_3a148219417a1e49384b08af03ba34cf;'#可变
                 ' mars_sid=d48a073e44172f33b579f8ee3f9383f5;'#可变
                 ' visit_id=785B557A8D187F54175ACE6036837FD5;' #可变
                 ' wap_consumer=A1; WAP_u_new=newone',
}
w=requests.post(url=ur,headers=head,data=json.dumps(data),verify=False)
print(json.loads(w.text))