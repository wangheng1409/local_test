#coding:utf-8
# a=1
# import pdb;pdb.set_trace()
# a=2
#
# s=[]
# t=not s and not s.append(1
# import copy
# a=[[1,2],[3,4]]
# b=copy.copy(a)
# c=copy.deepcopy(a)
# print(id(a),id(b),id(c))
# b[0][1]=5
# print(a,b,c,sep='\n')
#
# import sys
#      #5
#
# def f():
#     d = dict()
#     print(id(d))
#     d['a'] = 1
#     print(id(d['a']))
#     return d['a']
#
# b = f()
# print(id(b))
# print(sys.getrefcount(3),sys.getrefcount(b))


# import os
# if 'linux' in os.uname().sysname.lower():
#     MONGODB_URI=1
# else:
#     MONGODB_URI =2
#
# import requests
# import chardet
# url='http://jzdisplay.58.com/lmtj_ad.json?callback=jz_bottom_addata&req=%7B%22dispcateid%22%3A13915%2C%22displocalid%22%3A%224%22%2C%22pagetype%22%3A1%2C%22picsize%22%3A2%2C%22isbiz%22%3A2%2C%22pn%22%3A1%2C%22platform%22%3A0%2C%22slotids%22%3A%221000067%22%2C%22url%22%3A%22http%3A%2F%2Fm.58.com%2Fsz%2Fzplvyoujiudian%2F%3Freform%3Dpcfront%26PGTID%3D0d002408-0000-0202-8461-5b4d4c0eafed%26ClickID%3D1%22%7D'
# html = requests.get(url).content.decode()
# print(html)
# print(chardet.detect(html))
#
# with open('html.html', 'w+') as f:
#     f.write(html)
#
# from urllib import parse
# import chardet
# result = parse.urlparse('https://s.2.taobao.com/list/list.htm?spm=2007.1000261.0.0.MT56Id&catid=50100406&ist=1')
# print(result)
# params = parse.parse_qs(result.query, True)
# del params['spm']
# print(params)
# catid=params.get('catid',[])[0] if params.get('catid',[]) else ''
# ur=result.scheme+'://'+result.netloc+result.path+'?'+'&'.join(['%s=%s' %(k,v[0]) for k,v in params.items() ])
# print(ur)

# q=params.get('q',[])[0] if params.get('q',[]) else ''
# q=parse.unquote(q,encoding='gbk').strip(',')
# q=parse.quote(q,encoding='gbk')


# import time
# page=0
# t = str(time.time()).replace('.', '')
# ur='https://s.2.taobao.com/list/waterfall/waterfall.htm?' \
#            'wp='+str(page)+'&' \
#            '_ksTS='+t[:-3]+'_'+t[-3:]+'&' \
#            'callback=jsonp131&' \
#            'stype=1&' \
#            'catid='+str(catid)+'&' \
#             'q=' + str(q) + '&' \
#             'st_trust=1&ist=0'
# print(ur)
# print(catid,q)


# import os
#
# print(os.environ.get('PYDEVD_USE_FRAME_EVAL'))

# import contextlib
#
# @contextlib.contextmanager
# def worker_state(x,v):
#     x.append(v)
#     try:
#         yield
#     finally:
#         x.remove(v)
# with worker_state([],1) :
#     pass

# s=['a','b']
# d=sum(s[str],'')
# print(d)
# m=1
# def outer():
#     x,y,z=1,2,3
#     def inner():
#         print(y,z)
#         print(m)
#     return inner
# f=outer()
# print(f.__closure__)     #(<cell at 0x10ae50288: int object at 0x10acf7ae0>, <cell at 0x10aed00a8: int object at 0x10acf7b00>)
# print(f.__closure__[0].cell_contents)   #2
# print([x.cell_contents for x in f.__closure__]) #[2, 3] 即保存的值

#
# class A:
#     def __enter__(self):
#         print('start')
#         return 1
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print('end')
#         return 0
#
# with A():
#     print('function')
# #
# class DummyResource:
#     def __init__(self, tag):
#         self.tag = tag
#         print ('Resource [%s]' % tag)
#     def __enter__(self):
#         print('[Enter %s]: Allocate resource.' % self.tag)
#         return self   # 可以返回不同的对象
#     def __exit__(self, exc_type, exc_value, exc_tb):
#         print ('[Exit %s]: Free resource.' % self.tag)
#         if exc_tb is None:
#             print ('[Exit %s]: Exited without exception.' % self.tag)
#         else:
#             print ('[Exit %s]: Exited with exception raised.' % self.tag)
#             return False   # 可以省略，缺省的None也是被看做是False
#
# with DummyResource('normal'):
#     print(1)

# class DummyResource:
#
#     def __enter__(self):
#         print('[Enter %s]: Allocate resource.' % 'a')
#         return self   # 可以返回不同的对象
#     def __exit__(self, exc_type, exc_value, exc_tb):
#         print ('[Exit %s]: Free resource.' % 'a')
#         if exc_tb is None:
#             print ('[Exit %s]: Exited without exception.' % 'a')
#         else:
#             print ('[Exit %s]: Exited with exception raised.' % 'a')
#             return False   # 可以省略，缺省的None也是被看做是False
#
# with DummyResource():
#     print(1)

# from contextlib import contextmanager
#
#
# @contextmanager
# def demo():
#     print(
#     '[Allocate resources]')
#     print(
#     'Code before yield-statement executes in __enter__')
#     yield '*** contextmanager demo ***'
#     print(
#     'Code after yield-statement executes in __exit__')
#     print(
#     '[Free resources]')
#
#
# with demo() as value:
#     print(
#     'Assigned Value: %s' % value)

#
# def outer1(func):
#     def inner():
#         print('a')
#         func()
#         print('b')
#     return inner
#
# def outer2(func):
#     def inner():
#         print('c')
#         func()
#         print('d')
#     return inner
# def outer3(func):
#     def inner():
#         print('e')
#         func()
#         print('f')
#     return inner
# @outer1
# @outer2
# @outer3
# def func():
#     pass
# func()

# class X:
#     def __init__(self,arg):
#         self.arg=arg
#     def test(self,arg):
#         def outer(func):
#             def inner(*arg, **kwargs):
#                 print(1)
#             return inner
#         return outer
#
# x=X(1)
# @x.test(2)
# def func():
#     pass

# d = {1: "a", 2: "b", 3: {4: "c", 5: "d", 6: {7: "e"}}, 8: "f"}
#
#
# def func(kk,dic):
#     for k,v in dic.items():
#         if isinstance(v,dict):
#             func([i for i in kk+[k]],v)
#         else:
#             print(','.join([str(i) for i in kk+[k,v]]))
# func([],d)

# def func(kk,dic):
#     for k,v in dic.items():
#         if isinstance(v,dict):
#             k_list=[] if not kk else kk
#             k_list.append(k)
#             func(k_list,v)
#         else:
#             print(','.join([str(i) for i in kk+[k,v]]))
# func([],d)

# def func1(kk,dic):
#     for k,v in dic.items():
#         if isinstance(v,dict):
#             func1('%s,%s'%(kk,k),v)
#         else:
#             print(','.join([kk,str(k),str(v)])[1:])
# func1('',d)
#
#
# s=[]
# print(s if not s.append(1) else '')
# import traceback
# import logging
# try:
#     print(a)
# except Exception as e:
#     logging.error(traceback.format_exc())
# print(123)

# import grequests
# urls=[]
# rs = (grequests.get(u) for u in urls)
# rs = grequests.map(rs)
# import grequests
# import time
#
# t1 = time.time()
# urls = ['https://detail.m.tmall.com/item.htm?id=%s' % (538419935978) ]*50
# rs = (grequests.get(u) for u in urls)
# a=grequests.map(rs)
#
# t2 = time.time()
#
# print('-'*10, t2-t1)

a='''
'raw' : '[
        {'desc': '[宝山吴淞] [上海市] [宝山吴淞]的派件已签收 感谢使用中通快递,期待再次为您服务!', 'time': '1497415599'},
        {'desc': '[宝山吴淞] [上海市] [宝山吴淞]的付小胖1正在第1次派件 电话:13918969804 请保持电话畅通、耐心等待', 'time': '1497397744'},
        {'desc': '[宝山吴淞] [上海市] 快件到达 [宝山吴淞]', 'time': '1497396541'},
        {'desc': '[上海] [上海市] 快件离开 [上海]已发往[宝山吴淞]', 'time': '1497385681'}, 
        {'desc': '[上海] [上海市] 快件到达 [上海]', 'time': '1497383204'}, 
        {'desc': '[无锡中转部] [无锡市] 快件离开 [无锡中转部]已发往[上海]', 'time': '1497371702'},
        {'desc': '[无锡中转部] [无锡市] 快件到达 [无锡中转部]', 'time': '1497371647'}, 
        {'desc': '[常熟] [苏州市] 快件离开 [常熟]已发往[上海]', 'time': '1497357507'}, 
        {'desc': '[常熟] [苏州市] 快件到达 [常熟]', 'time': '1497357454'},
        {'desc': '[常熟天猫淘宝二] [苏州市] [常熟天猫淘宝二]的刘雷已收件 电话:18915663111', 'time': '1497355138'}
     ]'
'''


import re
def baidu(a):
    phone = re.findall(r'电话:(\d+)', a)
    print(phone)
    name1 = re.findall(r'的(.*?)已收件', a)
    print(name1)

    name2 = re.findall(r'的(.*?)正在', a)
    print(name2)


b = '''
  "<div class=\"fl w540 querycont morequerycont none\">\n
<h3>运单号：434855360077</h3>\n  
<input id=\"Status\" style=\"display: none\" value=\"签收\">\n 
\n                <div class=\"queryinfor clearfix h100\">\n  
<ul>\n                        <li style=\"border-left: none;\">\n  
<div class=\"img\">\n   
<a class=\"pingfen\">\n 
  <img src=\"/Content/themes/ztotheme/Images/billsearch_time.png\" width=\"35\" height=\"35\"></a>\n
</div>\n                            <div class=\"text3\">1天23小时</div>\n
</li>\n
<li>\n
<div class=\"img\">\n 
 <a class=\"pingfen pjsTel3\">\n 
<img src=\"/Content/themes/ztotheme/Images/billsearch_state.png\" width=\"35\" height=\"35\">\n   
</a>\n         
</div>\n  
<div class=\"text3\">\n签收\n
</div>\n
</li>\n 
<li>\n
<div class=\"img\" style=\"\">\n
<img src=\"/Content/themes/ztotheme/Images/BillSub.png\" width=\"43\">\n
</div>\n 
<div class=\"text3\">单号订阅</div>\n
</li>\n\n
<li>\n
<div class=\"img\">\n
<a>\n
<img class=\"pingfen\" id=\"pingfen3\" src=\"/Content/themes/ztotheme/Images/pingfen/pingfen.png\" width=\"41\"></a>\n\n
<script type=\"text/javascript\">\n
$(\"#pingfen3\").click(function () {\n 
$.layer({\n 
type: 2,\n
title: \"我要评分\",\n 
area: ['650px', '420px'],\n 
border: [0], //去掉默认边框\n  
iframe: { src: '/GuestService/BillDetails?BillCode=434855360077&BeginSite=太原兴华街&DeliverySite=新乡&TimeSpan=1.23:07:27&IpAddress=59.47.209.98, 175.102.16.21&Status=签收' }\n 
});\n     
$(\".xubox_page\").css(\"width\", \"100%\");\n   
$(\".xubox_title\").css({ \"border-radius\": \"8px 8px 0px 0px\" });\n   
$(\".xubox_main\").css({ \"border-radius\": \"8px\" });\n  
});\n      
</script>\n   
</div>\n           
<div class=\"text3 pingfen\">投诉评分</div>\n              
</li>\n\n\n          
</ul>\n      
</div>\n   
<div class=\"state\">\n 
<ul>\n   
<li class=\"pr firstChild current1\">\n\n    
<div class=\"on\"><span style=\"color:red\">[太原市] </span> 快件已在 <a data-sitecode=\"35142\" data-sitetel=\"0351-2781552\" class=\"routeTips\">太原兴华街</a> 签收 签收人: <a data-billcode=\"434855360077\" class=\"routeTips\" data-sitename=\"太原兴华街\">本人</a>,感谢您使用中通快递，期待再次为您服务!Delivered.</div>\n        
<div class=\"time\">2017-04-20 17:44:17</div>\n 
</li> \n         
<li class=\"pr \">\n\n 
<div class=\"\"><span style=\"color:red\">[太原市] </span>快件已经到达 <a data-sitecode=\"35142\" data-sitetel=\"0351-2781552\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=13753127162\" class=\"routeTips\">太原兴华街</a>Arrival at inward office of exchange.</div>\n 
<div class=\"time\">2017-04-20 15:27:08</div>\n 
</li> \n 
<li class=\"pr \">\n\n  
<div class=\"\"><span style=\"color:red\">[太原市] </span><a data-sitecode=\"35142\" data-sitetel=\"0351-2781552\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=18636116586\" class=\"routeTips\">太原兴华街</a> 的 <a class=\"routeTips\">张艳军[18636116586]</a> 正在派件Physical delivery scheduled.</div>\n                                    <div class=\"time\">2017-04-20 15:22:51</div>\n                                </li> \n                                <li class=\"pr \">\n\n                                    <div class=\"\"><span style=\"color:red\">[太原市] </span>快件离开 <a data-sitecode=\"35100\" data-sitetel=\"\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=18636145008\" class=\"routeTips\">太原中转</a> 已发往 <a data-sitecode=\"35142\" data-sitetel=\"0351-2781552\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=18636145008\" class=\"routeTips\">太原兴华街</a>Departure from inward office of exchange.</div>\n 
<div class=\"time\">2017-04-20 12:46:43</div>\n  
</li> \n            
<li class=\"pr \">\n\n 
<div class=\"\"><span style=\"color:red\">[太原市] </span>快件已经到达 <a data-sitecode=\"35100\" data-sitetel=\"\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=18235584242\" class=\"routeTips\">太原中转</a>Arrival at inward office of exchange.</div>\n                                    <div class=\"time\">2017-04-20 11:19:01</div>\n                                </li> \n                                <li class=\"pr \">\n\n                                    <div class=\"\"><span style=\"color:red\">[郑州市] </span>快件离开 <a data-sitecode=\"37100\" data-sitetel=\"\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=18336442700\" class=\"routeTips\">郑州中转</a> 已发往 <a data-sitecode=\"35100\" data-sitetel=\"\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=18336442700\" class=\"routeTips\">太原中转</a>Departure from inward office of exchange.</div>\n                                    <div class=\"time\">2017-04-19 09:14:04</div>\n                                </li> \n                                <li class=\"pr \">\n\n                                    <div class=\"\"><span style=\"color:red\">[郑州市] </span>快件已经到达 <a data-sitecode=\"37110\" data-sitetel=\"0371-63333286\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=15290896868\" class=\"routeTips\">郑州</a>Arrival at inward office of exchange.</div>\n                                    <div class=\"time\">2017-04-19 09:12:56</div>\n                                </li> \n                                <li class=\"pr \">\n\n                                    <div class=\"\"><span style=\"color:red\">[新乡市] </span>快件离开 <a data-sitecode=\"37310\" data-sitetel=\"0373-3528448、0373-3528446\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=13523733703\" class=\"routeTips\">新乡</a> 已发往 <a data-sitecode=\"35110\" data-sitetel=\"\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=13523733703\" class=\"routeTips\">太原</a>Departure from inward office of exchange.</div>\n                                    <div class=\"time\">2017-04-18 19:52:09</div>\n                                </li> \n                                <li class=\"pr \">\n\n                                    <div class=\"\"><span style=\"color:red\">[新乡市] </span><a data-sitecode=\"37310\" data-sitetel=\"0373-3528448、0373-3528446\" target=\"_blank\" style=\"color:red\" href=\"http://www.kuaidihelp.com/wangdian/kdyDetail?mobile=18103739596\" class=\"routeTips\">新乡</a> 的  <a class=\"routeTips\">大学城分部[18103739596]</a> 已收件Parcel scanned by site.</div>\n                                    <div class=\"time\">2017-04-18 18:36:50</div>\n                                </li> \n\n                        </ul>\n                </div>\n            </div>",

'''
#
# c='：13918969804 '
# def zto(b):
#     phone1 = re.findall(r'13[0-9]{9}|15[012356789][0-9]{8}|18[0-9]{9}|14[579][0-9]{8}|17[0-9]{9}', b)
#     print(phone1)
#
#
# zto(a)
# baidu(a)
#
#
#
# s=[x for x in range(10000)]  #需要切的列表
# t=[]
# _slice=1000
# for i in range(len(s)//_slice):
#     a=s[:_slice]
#     del s[:_slice]
#     t.append(a)
# print(t)
#
# from concurrent import futures
# import requests
# def func():
#     url = 'https://detail.m.tmall.com/item.htm?id=%s' % (538419935978)
#     print('GET: %s' % url)
#     data = requests.get(url).content
#
# workers=10
# with futures.ProcessPoolExecutor(workers) as excutor:
#     futs={excutor.submit(func) for i in range(100)}
#
#     result=[fut.result() for fut in futs]

#
# a=[]
# def func():
#     global a
#     for i in range(10):
#         a.append(1)
#         if len(a)==2:
#             print(len(a))
#             a=[]
# func()
# import datetime
# import time
#
# s=int(time.time())
# print(s)
# print(datetime.datetime.utcfromtimestamp(s+3600*8))
#
# print(int('0x59b9ef42',16))
#
# start=1505292041
# end=1505357634
# print([x for x in range(start,end,86400)]+[end])
#
# s=time.mktime(time.strptime('2017-09-14', "%Y-%m-%d"))
# print(s)
#
# print('CONCURRENT_REQUESTS'.lower())
#
# delay_list=[0,1,2,5]
# concurrent_requests_list=[10,20,30,40,50]
# run_list=[]
# for d in delay_list:
#     for c in concurrent_requests_list:
#         run_list.append((d,c))
# print(run_list)
s={1:1}