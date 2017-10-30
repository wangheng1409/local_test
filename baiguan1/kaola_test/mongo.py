# !/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo

client = pymongo.MongoClient('mongodb://root:big_one_112358@123.59.69.66:5600')
db = client['kaola']
goods_id_list=db.kaola_detail.distinct('goods_id')
complete_goods_list=db.kaola_sales.distinct('goodsId')
complete_page_list=db.kaola_page_detail.distinct('goodsId')

print(len(goods_id_list))
print(len(complete_goods_list))
print(len(complete_page_list))

det=set(goods_id_list)-set(complete_goods_list)-set(complete_page_list)
print(det)

