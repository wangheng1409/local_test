
# !/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import pymongo
import time
from bson import ObjectId
from concurrent.futures import ThreadPoolExecutor, as_completed
from pympler import summary
from pympler import muppy
import gc
import grequests
import requests
from collections import defaultdict
import copy
from bo_lib.general import ProxyManager
pm = ProxyManager()


class BaseBoStressTester():

    def __init__(self,url,headers,method,delay,concurrent_requests,test_times=1000,**data):
        self.url=url
        self.headers=headers
        self.method=method
        self.data=data
        self.complete_url_dic=defaultdict(int)
        self.delay=delay
        self.concurrent_requests=concurrent_requests
        self.size=concurrent_requests/10
        self.test_times=test_times

    def run(self):
        new_list, len_new_list=self.cut_list([self.url]*self.test_times)
        for cycle in self.gen_executor(self.find_detail, new_list):
            gc.collect()
            # summary.print_(summary.summarize(muppy.get_objects()), limit=4)
        return self.complete_url_dic

    def cut_list(self,old_list, _slice=1):
        new_list = []  # 切成功后的 ：[[],[],[],[]]
        for i in range(len(old_list) // _slice):
            a = old_list[:_slice]
            del old_list[:_slice]
            new_list.append(a)
        len_new_list = len(new_list) * _slice
        print('new_list ok', len_new_list)
        return new_list, len_new_list

    def find_detail(self,url_list):

        if self.method.lower()=='get':
            ret = (grequests.get(u, headers=self.headers, proxies=pm.getProxyV2(), timeout=10) for u in url_list)
            ret = grequests.imap(ret, size=self.size)
        else:
            ret = (grequests.post(u, headers=self.headers,data=self.data, proxies=pm.getProxyV2(), timeout=10) for u in url_list)
            ret = grequests.imap(ret, size=self.size)
        for i in ret:
            if i.status_code==200:
                self.complete_url_dic['delay'+str(self.delay)+'concurrent_requests'+str(self.concurrent_requests)]+=1
                if self.complete_url_dic['delay'+str(self.delay)+'concurrent_requests'+str(self.concurrent_requests)]%100==0:
                    print('delay'+str(self.delay)+'concurrent_requests'+str(self.concurrent_requests),
                          self.complete_url_dic[
                              'delay' + str(self.delay) + 'concurrent_requests' + str(self.concurrent_requests)]
                          )

        if self.delay:
            time.sleep(self.delay)

    def gen_executor(self,work, slice_list):
        workers = 10
        with ThreadPoolExecutor(workers) as executor:
            futures = [executor.submit(work, slice_item) for slice_item in slice_list]
            for future in as_completed(futures):
                futures.remove(future)
                yield

class BoStressTester():
    def __init__(self,url,headers,method,test_times=1000,**data):
        self.url = url
        self.headers = headers
        self.method = method
        self.data = data
        self.test_times=test_times
        self.delay_list = [0, 1, 2, 5]
        self.concurrent_requests_list = [10, 20, 30, 40, 50]
        self.run_list = []
        self.result_list = []
        for d in self.delay_list:
            for c in self.concurrent_requests_list:
                self.run_list.append((d, c))
    def run(self):
        for item in self.run_list:
            print(item[0], item[1])
            obj = BaseBoStressTester(self.url, self.headers, self.method, item[0], item[1], self.test_times,**self.data)
            self.result_list.append(dict(obj.run()))
            print(self.result_list)
        return {self.url:self.result_list}

if __name__ == '__main__':
    #get
    # xdf=BoStressTester(url='http://souke.xdf.cn/',
    #             headers={},
    #             method='get',
    #             test_times=1  #测试次数，默认1000
    #             )
    # print(xdf.run())

    #post
    # ofo=BoStressTester(url='https://san.ofo.so/ofo/Api/nearbyofoCar',
    #             headers={
    #                     'Host':	'san.ofo.so',
    #                     'Referer':	'https://common.ofo.so/newdist/?utm_source=download&utm_medium=smwappz&',
    #                     'Accept':	'*/*',
    #                     # 'Content-Type':	'multipart/form-data; boundary=----ofo-boundary-MC42MzU4MTY3',
    #                     'Accept-Language':	'zh-cn',
    #                     'Accept-Encoding':	'gzip, deflate',
    #                     'Origin':	'https://common.ofo.so',
    #                     'Content-Length':	'516',
    #                     'Connection' :'keep-alive',
    #                     'User-Agent':	'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/13A452 UCBrowser/10.7.0.643 Mobile'
    #                 },
    #             method='post',
    #             data={
    #                 'token'	:'307345E0-32C0-11E7-9270-234CDE175C92',
    #                 'source'	:0,
    #                 'source-version':	9999,
    #                 'lat'	:39.951834,
    #                 'lng':	116.417403,
    #             },
    #             test_times=1
    #             )
    # print(ofo.run())

    # tmtb=BoStressTester(url='https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=554781097315&sellerId=751796500&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess',
    #             headers={
    #                 'accept':'*/*',
    #                 'accept-encoding':'gzip, deflate, br',
    #                 'accept-language':'zh-CN,zh;q=0.8',
    #                 'cookie':'v=0; cookie2=1c7ae7be4a6fd210cd099bc6285e8d5c; t=d043ac5542cce176c9a040761684b15d; thw=cn; _m_h5_tk=36ef9bb8cb2b34d9e7ad28da509074d0_1505457872316; _m_h5_tk_enc=0ee46eb3096ada312ce7e747cac6320a; miid=1996970617266021810; isg=AhAQzygxfSisGCEEVEhMqpER4ViicedKGbckeArgemouRbTvsujcso-3azte; cna=7UIUEr29+A0CAXaQhSXRK9Rc; _tb_token_=f3333657e7e33; mt=ci%3D-1_0; uc1=cookie14=UoTcCi87CtVaEg%3D%3D',
    #                 'referer':'https://item.taobao.com/item.htm?spm=5148.10035500.848425.34.63348a62RWv21x&id=554781097315',
    #                 'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    #                 },
    #             method='get',
    #             test_times=10  #测试次数，默认1000
    #             )
    # print(tmtb.run())


    ya=BoStressTester(url='http://106.75.76.224',method='get',
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
    },test_times=100)
    print(ya.run())


