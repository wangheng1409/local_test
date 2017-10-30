# !/usr/bin/env python
# -*- coding:utf-8 -*-

# from pandas import DataFrame, read_csv
# import matplotlib.pyplot as plt
# import pandas as pd
# import sys
# import matplotlib
# import pickle
# names = ['Bob','Jessica','Mary','John','Mel']
# births = [968, 155, 77, 578, 973]
#
# BabyDataSet = list(zip(names,births))
#
#
# df = pd.DataFrame(data = BabyDataSet, columns=['Names', 'Births'])


import pymongo

#


# mongo = pymongo.MongoClient()
# db = mongo['privacy']['test']
# db.insert({'raw':'''raw' : '[
#         {'desc': '[宝山吴淞] [上海市] [宝山吴淞]的派件已签收 感谢使用中通快递,期待再次为您服务!', 'time': '1497415599'},
#         {'desc': '[宝山吴淞] [上海市] [宝山吴淞]的付小胖1正在第1次派件 电话:13918969804 请保持电话畅通、耐心等待', 'time': '1497397744'},
#         {'desc': '[宝山吴淞] [上海市] 快件到达 [宝山吴淞]', 'time': '1497396541'},
#         {'desc': '[上海] [上海市] 快件离开 [上海]已发往[宝山吴淞]', 'time': '1497385681'},
#         {'desc': '[上海] [上海市] 快件到达 [上海]', 'time': '1497383204'},
#         {'desc': '[无锡中转部] [无锡市] 快件离开 [无锡中转部]已发往[上海]', 'time': '1497371702'},
#         {'desc': '[无锡中转部] [无锡市] 快件到达 [无锡中转部]', 'time': '1497371647'},
#         {'desc': '[常熟] [苏州市] 快件离开 [常熟]已发往[上海]', 'time': '1497357507'},
#         {'desc': '[常熟] [苏州市] 快件到达 [常熟]', 'time': '1497357454'},
#         {'desc': '[常熟天猫淘宝二] [苏州市] [常熟天猫淘宝二]的刘雷已收件 电话:18915663111', 'time': '1497355138'}
#      ]'''
#                  })

import re
a='''
    [{'desc': '[陈辉] [无锡市] [陈辉]的派件已签收 感谢使用中通快递,期待再次为您服务!', 'time': '1494672003'},
    {'desc': '[陈辉] [无锡市] [陈辉]的陈亮15716172435正在第1次派件 电话:18151555937 请保持电话畅通、耐心等待', 'time': '1494671461'}, 
    {'desc': '[陈辉] [无锡市] 快件到达 [陈辉]', 'time': '1494639778'}, 
    {'desc': '[无锡] [无锡市] 快件离开 [无锡]已发往[无锡十七区]', 'time': '1494608730'}, 
    {'desc': '[无锡中转部] [无锡市] 快件离开 [无锡中转部]已发往[无锡]', 'time': '1494608212'},
    {'desc': '[无锡中转部] [无锡市] 快件到达 [无锡中转部]', 'time': '1494606004'}, 
    {'desc': '[潮汕中心] [揭阳市] 快件离开 [潮汕中心]已发往[无锡中转部]', 'time': '1494526337'},
    {'desc': '[潮汕中心] [揭阳市] 快件到达 [潮汕中心]', 'time': '1494526114'}, 
    {'desc': '[普宁] [揭阳市] 快件离开 [普宁]已发往[无锡]', 'time': '1494519489'},
    {'desc': '[普宁] [揭阳市] [普宁]的8907林煜栋已收件 电话:13542892639', 'time': '1494516101'}]

'''
# a=re.sub('13[0-9]{9}|15[012356789][0-9]{8}|18[0-9]{9}|14[579][0-9]{8}|17[0-9]{9}','kkk',a)
# print(a)
# b=re.sub('的(.{1,20})已收件','kkk',a)
# print(b)
# c=re.sub('的(.{1,20})正在','kkk',b)
# print(c)
#
# s='ab'
# s=s.replace('a','c')
# print(s)

# import random
# ran_list=[10,193,228,2227,5605,1834]
# for i in range(len(ran_list),1,-1):
#     ran_list[i-1]=sum(ran_list[:i])
# print(ran_list)
#
# a=random.randrange(0,10097)
# for i in range(len(ran_list)):
#     if a<ran_list[i]:
#         break
# print(i+1)
# start=ran_list[i-1]
# end=ran_list[i]
#
# print(start,end)

s='885686205649860945'
print(len(s))

s='3934483457167'
print(len(s))




