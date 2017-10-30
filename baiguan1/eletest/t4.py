# import pymongo
#
#
# client = pymongo.MongoClient(
#     'mongodb://root:Baiguan2016@60.205.152.167:3717')
# database = client.shengjian
#
# item = database.store_list.find_one({'store_id':122 },
#                                    {'delivery_mode': 1, 'supports': 1})


# import time
# import requests
#
# ret=requests.get('https://h5.m.taobao.com/app/waimai/list.html?'
#              'type=category'
#              '&id=1'
#              '&title=%E7%BE%8E%E9%A3%9F%E5%A4%96%E5%8D%96'
#              '&spm=a21he.7998619.0.i7998619').content
# print(ret.decode())

import requests
# print(requests.get('http://httpbin.org/status/419').text)

#
from odps import ODPS
o = ODPS('LTAIxrZjJRgoUked', 'RZKFDNUyScX9TX6UH2xJJmMsnwlfJ4',
   project='kysj')

dual = o.get_table('sj_menu')

print(dual.name)


