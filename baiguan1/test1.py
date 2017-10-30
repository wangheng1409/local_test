# import pymongo
# client=pymongo.MongoClient()
# database=client.shengjian
# col=database.store_list
# store_id_obj=col.find()
#
# s=store_id_obj
# # s={}
# # for store_item in store_id_obj:
# #     s[store_item['id']]=store_item
# #
# # s=s.values()
# j=0 #1
# k=[] #4
# w=[] #5 no
# z=[] #9 ok
# for i in s:
#     if i['status'] ==1:
#         j+=1
#     elif i['status']==4:
#         k.append(i)
#     elif i['status']==5:
#         w.append(i)
#     elif i['status']==9:
#         z.append(i)
# print(len(k),k,'\n',
#     len(w),w,'\n',
#       )


# store_id_obj=col.distinct('id')
# print(store_id_obj)
# store_id_list=[str(item['status']) for item in store_id_obj]
# print(store_id_list,len(store_id_list))
#
# # info_dict={'name':'hh','age':89,'sex':'unkonw','salary':8988}
# # col.insert(info_dict)
# #
# # item=col.find({'name':'hh'})
# # for i in item:
# #     print(i['salary'])
# #
# # col.update({'name':'q'},{'$set':{'age':99}})
# # col.delete_many({'name':'hh'})
#
# # data={'id':123,'name':'s','age':20,}
# # col.insert(data)
#
# # import  mongoengine
# import redis
# r=redis.StrictRedis(host='127.0.0.1',port=6379)
# import lxml
# import scrapy_redis.spiders

import requests
import json
# s=requests.get('https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wx4errgynr6&latitude=39.98993&limit=24&longitude=116.33965&offset=0&terminal=web').text
# s=json.loads(s)
# print(len(s),type(s),s[0])

{'activities': [{
    'attribute': '17.0',
    'description': '新用户下单立减17.0元',
    'icon_color': '70bc46',
    'icon_name': '新',
    'id': 26086140,
    'is_exclusive_with_food_activity': True,
    'name': '新用户立减(不与其他活动共享)',
    'tips': '新用户下单立减17.0元',
    'type': 103},
    {'attribute': '{"60": {"1": 12, "0": 0}}',
     'description': '满60减12',
     'icon_color': 'f07373',
     'icon_name': '减',
     'id': 27551041,
     'is_exclusive_with_food_activity': True,
     'name': '满减优惠', 'tips': '满60减12', 'type': 102},
    {'description': '517、特惠等你！！！',
     'icon_color': 'f07373',
     'icon_name': '饿',
     'id': 25762394,
     'name': '517、特惠等你！！！',
     'tips': '517、特惠等你！！！'},
    {'description': '517、我爱吃！！！',
     'icon_color': 'f07373', 'icon_name': '折',
     'id': 25762310, 'name': '517、我爱吃！！！',
     'tips': '517、我爱吃！！！'},
    {'description': '517、6.6？？？', 'icon_color': 'f1884f',
     'icon_name': '特', 'id': 25715201, 'name': '517、6.6？？？',
     'tips': '517、6.6？？？'}],
    'address': '北京市海淀区北京市海淀区中关村东路8号东升大厦C座平房02',
    'authentic_id': 1433283,
    'average_cost': '¥33/人',
    'delivery_mode': {'color': '57A9FF', 'id': 1, 'is_solid': True, 'text': '蜂鸟专送'},
    'description': '周黑鸭',
    'distance': 781,
    'float_delivery_fee': 5,
    'float_minimum_order_amount': 20,
    'id': 1433283,
    'image_path': '7537a93e77e68af227d6d8413d48cc4ejpeg',
    'is_new': False, 'is_premium': True, 'is_stock_empty': 0,
    'latitude': 39.99484,
    'longitude': 116.33308,
    'max_applied_quantity_per_order': -1,
    'name': '周黑鸭(北京清华大学店)',
    'next_business_time': '',
    'only_use_poi': False,
    'opening_hours': ['09:00/22:35'],
    'order_lead_time': 20,
    'phone': '13520525101',
    'piecewise_agent_fee':
        {'description': '配送费¥5',
         'extra_fee': 0, 'is_extra': False,
         'rules': [{'fee': 5, 'price': 20}],
         'tips': '配送费¥5'},
    'promotion_info': '贴心提示：满减代金卷可叠加使用，美食不等待~~',
    'rating': 5,
    'rating_count': 450,
    'recent_order_num': 1071,
    'recommend': {'image_hash': 'ff085f835038a87ae040a8cd53338f4cjpeg', 'track': '{"rankType":"3"}'},
    'regular_customer_count': 0, 'status': 1,
    'supports': [{'description': '已加入“外卖保”计划，食品安全有保障', 'icon_color': '999999', 'icon_name': '保', 'id': 7, 'name': '外卖保'}, {'description': '准时必达，超时秒赔', 'icon_color': '57A9FF', 'icon_name': '准', 'id': 9, 'name': '准时达'}], 'type': 0}

# store=requests.get('https://www.ele.me/restapi/shopping/restaurant/1433283?extras%5B%5D=activity&extras%5B%5D=license&extras%5B%5D=identification&extras%5B%5D=albums&extras%5B%5D=flavors&latitude=39.98993&longitude=116.33965').text
# # print(menu)
# store=json.loads(store)
# print(len(store),type(store),store)

{'address': '北京市海淀区中关村东路8号东升大厦C座平房02',
 'authentic_id': 1433283,
 'delivery_mode':
     {'color': '57A9FF',
      'id': 1,
      'is_solid': True, 'text': '蜂鸟专送'},
 'description': '周黑鸭',
 'distance': 781,
 'flavors': [{'id': 235, 'name': '鸭脖卤味'},
             {'id': 240, 'name': '奶茶果汁'}],
 'float_delivery_fee': 5,
 'float_minimum_order_amount': 20,
 'id': 1433283,
 'image_path': '7537a93e77e68af227d6d8413d48cc4ejpeg',
 'is_new': False,
 'is_premium': True,
 'is_stock_empty': 0,
 'latitude': 39.99484,
 'license': {'business_license_image': '9564503bb91903e9fb8e082580deef63jpeg',
             'catering_service_license_image': '001446d230c103f088a126ff40593294jpeg',
             'service_license_business_scope': '',
             'service_license_register_authority': '',
             'service_license_register_date': '1970-01-01'},
 'longitude': 116.33308,
 'max_applied_quantity_per_order': 1,
 'name': '周黑鸭(北京清华大学店)',
 'next_business_time': '',
 'only_use_poi': False,
 'opening_hours': ['09:00/22:35'],
 'order_lead_time': 20,
 'phone': '13520525101',
 'piecewise_agent_fee':
     {'description': '配送费¥5',
      'extra_fee': 0,
      'is_extra': False,
      'rules': [{'fee': 5, 'price': 20}],
      'tips': '配送费¥5'},
 'promotion_info': '贴心提示：满减代金卷可叠加使用，美食不等待~~',
 'rating': 5,
 'rating_count': 450,
 'recent_order_num': 1071,
 'regular_customer_count': 0,
 'status': 1,
 'supports': [{'description': '已加入“外卖保”计划，食品安全有保障', 'icon_color': '999999', 'icon_name': '保', 'id': 7, 'name': '外卖保'},
              {'description': '准时必达，超时秒赔', 'icon_color': '57A9FF', 'icon_name': '准', 'id': 9, 'name': '准时达'}], 'type': 0}

# menu=requests.get('https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=1433283').text
# # print(menu)
# menu=json.loads(menu)
# print(len(menu),type(menu),menu)


# print(requests.get('https://mainsite-restapi.ele.me/ugc/v2/restaurants/312002/ratings?has_content=true&offset=0&limit=10').text)
# import random
#
# def random_ssid():
#     s=[]
#
#     for i in range(32):
#         b = random.randint(1, 4)
#         if b in [1,2]:
#             a=chr(random.randint(97, 122))
#         else:
#             a=str(random.randint(0, 9))
#         s.append(a)
#     return ''.join(s)
#
# s=''.join(map(lambda i:chr(random.randint(97, 122)) if random.randint(1, 4) in [1,2] else str(random.randint(0, 9)),range(32)))
# print(s,len(s))
from bo_lib.general import ProxyManager
# import base64
#
# proxy_server = "http://proxy.abuyun.com:9020"
# proxy_user = "H4BVZ0310R9EG51D"
# proxy_pass = "7DC2E09E894A4D9E"
# proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")
http_proxy='http://123.57.221.137:31009'
# http_proxy='http://160.214.118.170:63000'
# import requests
# import json
# for i in range(1000):
#     print(i)
#     session=requests.session()
#     session.proxies = {
#         "http": http_proxy,
#     }
#     s=session.get('https://mainsite-restapi.ele.me/shopping/restaurants?'
#                    'latitude=39.94983339999999&longitude=116.41447&keyword=&offset=0&limit=20&extras[]='
#                    'activities&restaurant_category_ids[]=209&restaurant_category_ids[]=211&restaurant_category_ids[]'
#                    '=212&restaurant_category_ids[]=213&restaurant_category_ids[]=214&restaurant_category_ids[]=215&'
#                    'restaurant_category_ids[]=216&restaurant_category_ids[]=217&restaurant_category_ids[]=218&'
#                    'restaurant_category_ids[]=219&restaurant_category_ids[]=221&restaurant_category_ids[]=222&'
#                    'restaurant_category_ids[]=223&restaurant_category_ids[]=224&restaurant_category_ids[]=225&'
#                    'restaurant_category_ids[]=226&restaurant_category_ids[]=227&restaurant_category_ids[]=228&'
#                    'restaurant_category_ids[]=229&restaurant_category_ids[]=230&restaurant_category_ids[]=231&'
#                    'restaurant_category_ids[]=232&restaurant_category_ids[]=234&restaurant_category_ids[]=235&'
#                    'restaurant_category_ids[]=236&restaurant_category_ids[]=237&restaurant_category_ids[]=238&'
#                    'restaurant_category_ids[]=263&restaurant_category_ids[]=264&restaurant_category_ids[]=265&'
#                    'restaurant_category_ids[]=266&restaurant_category_ids[]=267&restaurant_category_ids[]=268&'
#                    'restaurant_category_ids[]=269')
#     if s.status_code == 200:
#         print(json.loads(s.text,encoding='utf8')[0])
#     else:
#         print(s.text)

from collections import defaultdict

s=defaultdict(defaultdict())