# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
import redis
import re
from lxml import html
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
from vip.items import VipItem
from vip.guan import d,e



class StockSpider(RedisSpider):
    name = "vipespider"
    allowed_domains = []
    start_urls = []
    dic={}
    head = {
        'Host': 'm.vip.com',
        'Connection': 'keep-alive',
        # 'Content-Length':'270',
        'Origin': 'https://m.vip.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate, br',
        # 'Origin-Referer':'https://m.vip.com/classify-list-78925-0-0-0-0-1-20.html?title=%E7%9F%AD%E8%A2%96T%E6%81%A4',
        # 'Referer':'https://m.vip.com/classify-list-78925-0-0-0-0-1-20.html?title=%E7%9F%AD%E8%A2%96T%E6%81%A4',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'WAP_ID=6d653eb613f43d95b122061474cbbb56d8b162d3;'
        # ' WAP[locateip]=2034598954%2C101101%2CVIP_BJ%2C;'
                  ' WAP[oxo_area]=101101%2C101101101%2C; '
                  '_smt_uid=5965ceb0.a4ccffc;'
                  ' WAP[%2Findex.html]=1; '
                  'source=www;'
                  ' WAP[back_act]=%2Fproduct-1291007-208970514.html;'  # 可变
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
                  ' mars_pid=57; '  # 可变
                  'mars_cid=1499847024497_3a148219417a1e49384b08af03ba34cf;'  # 可变
                  ' mars_sid=d48a073e44172f33b579f8ee3f9383f5;'  # 可变
                  ' visit_id=785B557A8D187F54175ACE6036837FD5;'  # 可变
                  ' wap_consumer=A1; WAP_u_new=newone',
    }
    def start_requests(self):
        u='https://h5.vip.com/api/category/category/getSellingCategorys/?app_name=&app_version=&mobile_channel=&hierarchy_id=&category_id=&warehouse=&mars_cid=&category_filter=&sale_for=&area_id=&from_url_go_api_switch=&preview_go_admin=&src=app&channel_id=&channel_name=&_t=1499847024437&_=1499847024437'
        yield scrapy.Request(url=u, callback=self.parse, dont_filter=True)

    def parse(self, response):  # 遍历所有的分类
        # print(response.text)
        di=json.loads(response.text)['data']
        li=di['cate_lv1'][1:]
        self.dic={str(a['categoryId']):a['name'] for a in li}
        # print(self.dic)

        for categoryId,category_name in [x for x in self.dic.items()][1:2]  if settings['TEST'] else (x for x in self.dic.items()):

            u='https://h5.vip.com/api/category/category/getSellingCategorysChildren/?' \
                'app_name=' \
                '&app_version=' \
                '&mobile_channel=' \
                '&hierarchy_id=' \
                '&category_id='+str(categoryId)+'&' \
                'warehouse=' \
                '&mars_cid=' \
                '&category_filter=' \
                '&sale_for=' \
                '&area_id=' \
                '&from_url_go_api_switch=' \
                '&preview_go_admin=' \
                '&src=app' \
                '&channel_id=' \
                '&channel_name=' \
                '&_t=1499847515216&_=1499847515217'

            yield scrapy.Request(url=u, callback=self.get_category, dont_filter=True,
                                meta={'categoryId': categoryId,'category_name': category_name,
                                      })

    def get_category(self, response):
        categoryId = response.meta['categoryId']
        category_name = response.meta['category_name']
        # print(response.text)
        li = json.loads(response.text)['data']['current_node']['children']
        s=[ x for y in li for x in y['children'] ]
        for product_ty in s  if settings['TEST'] else s:
            ty_id=product_ty['categoryId']
            ty_name=product_ty['name']

            page = 1
            if ty_name in ['健身馆','露营馆','骑行馆',]:
                continue
            if '馆' in ty_name:
                if ty_name in ['韩国馆','日本馆','美洲馆']:
                    ur = 'https://m.vip.com/server.html?rpc&method=getClassifyList&f=&_=' + str(time.time()).replace('.', '')[:-3]
                    for ty_id,query in d[ty_name]:
                        data = {
                            "method": "getClassifyList",
                            "params": {
                                "page": "classify-list-" + str(ty_id) + "-0-0-0-0-1-20.html",
                                "np": str(page),
                                "ep": str(20),
                                "category_id": "",
                                "brand_store_sn": "",
                                "filter": "",
                                "sort": "0",
                                "minPrice": "",
                                "maxPrice": "",
                                "query": query
                            },
                            "id": str(time.time()).replace('.', '')[:-3],
                            "jsonrpc": "2.0"
                        }
                        yield scrapy.FormRequest(ur, callback=self.get_page,
                                                 headers=self.head,
                                                 body=json.dumps(data),
                                                 meta={'categoryId': categoryId,
                                                       'category_name': category_name,
                                                       'page':page,
                                                       'data':data,
                                                       'ty_name':ty_name,

                                                       },
                                                 dont_filter=True)
                else:
                    for s in e[ty_name]:
                        ur=s %(str((page-1)*50))
                        yield scrapy.Request(url=ur, callback=self.get_guan_page, dont_filter=True,
                                             meta={'categoryId': categoryId,
                                                   'category_name': category_name,
                                                   's': s,
                                                   'page': page,
                                                   'ty_name': ty_name,
                                                   })
            else:
                ur = 'https://m.vip.com/server.html?rpc&method=getClassifyList&f=&_=' + str(time.time()).replace('.','')[:-3]
                data = {
                    "method": "getClassifyList",
                    "params": {
                        "page": "classify-list-" + str(ty_id) + "-0-0-0-0-1-20.html",
                        "np": str(page),
                        "ep": str(20),
                        "category_id": "",
                        "brand_store_sn": "",
                        "filter": "",
                        "sort": "0",
                        "minPrice": "",
                        "maxPrice": "",
                        "query": "title=" + '%E7%9F%AD%E8%A2%96T%E6%81%A4'
                    },
                    "id": str(time.time()).replace('.', '')[:-3],
                    "jsonrpc": "2.0"
                }
                yield scrapy.FormRequest(ur,callback=self.get_page,
                                         headers=self.head,
                                          body=json.dumps(data),
                                          meta={'categoryId': categoryId,
                                                'category_name': category_name,
                                                'page':page,
                                                'data': data,
                                                'ty_name': ty_name,
                                          },
                                          dont_filter=True)

    def get_page(self, response):
        categoryId = response.meta['categoryId']
        category_name = response.meta['category_name']
        page = response.meta['page']
        data = response.meta['data']
        ty_name = response.meta['ty_name']
        # print(response.text)
        li = json.loads(response.text)[0]['result']['products']
        for product in li:
            l=len(product)
            if len(product)<10:
                continue
            product['categoryId']=categoryId
            product['category_name']=category_name
            product['ty_name']=ty_name
            product['page'] = page
            # item=VipItem()
            # item['detail']=product
            product_id=product['product_id']
            ur='https://stock.vip.com/detail/?callback=stock_detail&merchandiseId='+str(product_id)+'&is_old=0&_='+str(time.time()).replace('.', '')[:-3]
            yield scrapy.Request(url=ur, callback=self.stock_detail, dont_filter=True,
                                 meta={'product': product,
                                       })
        if li:
            ur=response.url
            page+=1
            data['params']['np']=str(page)
            yield scrapy.FormRequest(ur, callback=self.get_page,
                                     headers=self.head,
                                     body=json.dumps(data),
                                     meta={'categoryId': categoryId,
                                           'category_name': category_name,
                                           'page': page,
                                           'data': data,
                                           'ty_name': ty_name,
                                           },
                                     dont_filter=True)

    def stock_detail(self, response):
        product = response.meta['product']
        li=json.loads(response.text[13:-1])['items']
        num={a['name']:'' if a['stock']==11 else a['stock'] for a in li}
        product['num']=num
        if product['category_name']in ['美妆个护','唯品国际']:
            product_id=product['product_id']
            brand_id=product['brand_id']
            if product['category_name'] == '美妆个护':
                ur='http://detail.vip.com/detail-'+str(brand_id)+'-'+str(product_id)+'.html'
            else:
                ur='http://www.vip.com/detail-'+str(brand_id)+'-'+str(product_id)+'.html'
            yield scrapy.Request(url=ur, callback=self.beauty, dont_filter=True,
                                 meta={'product': product,
                                       })
        else:
            item=VipItem()
            item['detail']=product
            yield item

    def beauty(self, response):
        product = response.meta['product']

        try:
            country=response.xpath('//p[@class="global-name"]/text()').extract()[0]
            product['country_name'] = country.strip()
        except:
            pass
        try:
            buys_num = response.xpath('//span[@class="buy-num"]/text()').extract()[0]
            product['buys_num'] = int(buys_num)
        except:
            pass

        item = VipItem()
        item['detail'] = product
        yield item

    def get_guan_page(self,response):
        categoryId = response.meta['categoryId']
        category_name = response.meta['category_name']
        s = response.meta['s']
        page = response.meta['page']
        ty_name = response.meta['ty_name']
        page+=1
        next_ur=s %(str((page-1)*50))
        try:
            left=response.text.index('{')
            dic=json.loads(response.text[left:-1])
        except:
            print('json error',response.text[41:-1])
            dic={}

        for product in dic['data']:
            if len(product)<10:
                continue
            product['categoryId']=categoryId
            product['category_name']=category_name
            product['page']=page
            product['ty_name']=ty_name

            product_id = product['product_id']

            ur = 'https://stock.vip.com/detail/?callback=stock_detail&merchandiseId=' + str(
                product_id) + '&is_old=0&_=' + str(time.time()).replace('.', '')[:-3]
            yield scrapy.Request(url=ur, callback=self.stock_detail, dont_filter=True,
                                 meta={'product': product,
                                       })
        if dic['data']:
            yield scrapy.Request(url=next_ur, callback=self.get_guan_page, dont_filter=True,
                                 meta={'categoryId': categoryId,
                                       'category_name': category_name,
                                       's': s,
                                       'page': page,
                                       'ty_name': ty_name,
                                       })


    # def retry_this_poi(self, dic):
    #     # self.r.sadd('set' + self.redis_key, json.dumps(dic).encode("utf-8"))
    #     pass




