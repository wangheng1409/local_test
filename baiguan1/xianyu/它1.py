# !/usr/bin/env python
# -*- coding:utf-8 -*-

import grequests
import requests
import time
import datetime
import redis
import json
import pymongo
import re
import gc
import sys
import copy
import threading
from pympler import summary
from pympler import muppy
from urllib import parse
from bo_lib.general import ProxyManager
from concurrent.futures import ThreadPoolExecutor, as_completed

TEST = False
index = sys.argv[1] if not TEST else 0
start = time.time()
pm = ProxyManager()

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
}


class XianyuSpider():
    client = pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
    db = client.xianyu.xianyu_detail1
    redis_key = 'two_xianyuspider_redis'
    if not TEST:
        pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
    else:
        pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
    r = redis.Redis(connection_pool=pool)

    def __init__(self):
        self.urls = []
        self.finish_url_num = 0
        self.insert_list = []
        self.len_new_list = 0
        self.catagory_dic = {
            '50100408': '家用电器',
            '50100406': '居家日用',
            '50100409': '母婴',
            '50100405': '美容/美颜/香水',
            '50100398': '手机',
            '50100401': '相机/摄像机',
            '50100402': '笔记本电脑/电脑周边',
            '50100403': '随身影音娱乐',
            '50100411': '卡券/文体/户外/宠物',
            '50446013': '女装',
            '50100415': '珠宝/收藏',
            '50448012': '鞋包配饰',
        }

    def work(self, slice_item):
        ret = (grequests.get(u, headers=headers, proxies=pm.getProxyV2(), timeout=10) for u in slice_item)
        ret = grequests.imap(ret, size=100)
        for i in ret:
            if 'numFound' in i.text:
                self.finish_url_num += 1
                if self.finish_url_num % 100 == 0:
                    print(time.time() - start)
                left = i.text.index('{')
                try:
                    dic = json.loads(i.text[left:].strip()[:-1].replace('\\', '/'))
                except Exception as e:
                    print(e, 'json error', i.text)
                    dic = {'idle': []}
                    print('ok')
                print(self.finish_url_num, self.finish_url_num / self.len_new_list, '=' * 20, dic['numFound'],
                      len(dic['idle']), len(self.insert_list))
                result = parse.urlparse(i.url)
                params = parse.parse_qs(result.query, True, encoding='gb2312')
                catid = params.get('catid', [])[0] if params.get('catid', []) else ''
                self.jsonp_handle(dic,catid)
            else:
                print(i)
                print(i.url)

    def jsonp_handle(self, dic, catid):
        if dic['idle']:
            for item_dic in dic['idle']:
                try:
                    s = {}
                    s['category_name'] = self.catagory_dic[str(catid)]
                    s['catid'] = catid
                    s['user_name'] = item_dic['user']['userNick']
                    s['vipLevel'] = item_dic['user']['vipLevel']
                    s['title'] = item_dic['item']['title']
                    s['city'] = item_dic['item']['provcity']
                    s['time'] = item_dic['item']['publishTime']
                    s['commentCount'] = item_dic['item']['commentCount']
                    s['collectCount'] = item_dic['item']['collectCount']
                    s['price'] = float(item_dic['item']['price']) if item_dic['item']['price'] else 0
                    s['orgPrice'] = float(item_dic['item']['orgPrice']) if item_dic['item']['orgPrice'] else 0
                    s['itemUrl'] = 'https:' + item_dic['item']['itemUrl']
                    s['itemid'] = re.findall('id=(\d+)&', item_dic['item']['itemUrl'])[0]
                    s['ts_string'] = str(datetime.date.today())
                    s['ts'] = datetime.datetime.fromtimestamp(time.time(), None)
                    self.insert_list.append(s)

                    if len(self.insert_list) == 100:
                        tmp = self.insert_list[:]
                        del self.insert_list[:100]
                        self.db.insert_many(tmp)
                        print('+++++++++++')
                except Exception as e:
                    print(e, item_dic)
        else:
            print(dic['idle'])

    def get_all_page_num(self, ur,category_name):
        try:
            ret = requests.get(ur, headers=headers, proxies=pm.getProxyV2(), timeout=200).text
            left = ret.index('{')
            try:
                dic = json.loads(ret[left:].strip()[:-1].replace('\\', '/'))
            except Exception as e:
                print(e, 'json error', ret)
                dic = json.loads(ret[left:].strip()[:-1].replace('\\', '/'))
                print('ok')
            try:
                all_page = dic['totalPage']
            except:
                all_page = -1
            if all_page == -1:
                all_page=self.get_all_page_num( ur,category_name)
            else:
                return all_page
        except:
            all_page = self.get_all_page_num(ur, category_name)
        print(category_name,all_page)
        return all_page

    def generate_url_allpage(self, catid, all_page, t):
        for i in range(all_page):
            ur = 'https://s.2.taobao.com/list/waterfall/waterfall.htm?' \
                 'wp=' + str(i) + '&' \
                                  '_ksTS=' + t[:-3] + '_' + t[-3:] + '&' \
                                                                     'callback=jsonp114&' \
                                                                     'stype=1&' \
                                                                     'catid=' + str(catid) + '&' \
                                                                                             'st_trust=1&ist=1'
            self.urls.append(ur)

    def cut_list(self, old_list, _slice=1000):
        new_list = []  # 切成功后的 ：[[],[],[],[]]
        for i in range(len(old_list) // _slice):
            a = old_list[:_slice]
            del old_list[:_slice]
            new_list.append(a)
        len_new_list = len(new_list) * 1000
        print('new_list ok', len_new_list)
        return new_list, len_new_list

    def gen_executor(self, slice_list):
        workers = 10
        with ThreadPoolExecutor(workers) as executor:
            futures = [executor.submit(self.work, slice_item) for slice_item in slice_list]
            for future in as_completed(futures):
                futures.remove(future)
                yield

    def run(self):
        data_list = self.r.lrange(self.redis_key, index, int(index) + 2)
        for data in data_list:
            store_item = json.loads(data.decode(), encoding='utf-8')
            category_name = store_item['category_name']
            catid = store_item['catid']
            page = store_item['page']
            referer = store_item['referer']
            headers.update({'referer': referer})
            t = str(time.time()).replace('.', '')
            ur = 'https://s.2.taobao.com/list/waterfall/waterfall.htm?' \
                 'wp=' + str(page) + '&' \
                '_ksTS=' + t[:-3] + '_' + t[-3:] + '&' \
                'callback=jsonp114&' \
                'stype=1&' \
                'catid=' + str(catid) + '&' \
                'st_trust=1&ist=1'
            all_page = self.get_all_page_num(ur,category_name)
            self.generate_url_allpage(catid, all_page, t)
        new_list, self.len_new_list = self.cut_list(self.urls)

        for cycle in self.gen_executor(new_list):
            gc.collect()
            summary.print_(summary.summarize(muppy.get_objects()), limit=4)


if __name__ == '__main__':
    xianyu = XianyuSpider()
    xianyu.run()
    print(time.time() - start)
