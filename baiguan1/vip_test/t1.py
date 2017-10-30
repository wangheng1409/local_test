#
# import pymongo
# import datetime,time
# from collections import defaultdict
#
# client=pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
# database=client.vip
# print(str(datetime.date.today()))
# col=database.vip_detail.find({},{'_id':0,'category_name':1,'product_id':1})
# s={}
#
# category_num=defaultdict(int)
#
# c = 0
# for item in col:
#     if c % 10000 == 0:
#         print('count', c)
#     c+=1
#     try:
#         s[item['product_id']]=item
#     except:
#         print(item)
#
# l=list(s.values())
# for item in l:
#     category_num[item['category_name']]+=1
#
# print(category_num)

# menu=database.store_menu_list.find({'ts_string':str(datetime.date.today())}).count()

# category_num0=defaultdict(int)
# c = 0
# for item in col:
#     if c % 10000 == 0:
#         print('count', c)
#     c+=1
#     try:
#         category_num0[item['category_name']]+=1
#     except:
#         print(item)
# print(category_num0)

s=[1,2,3]
print(s[:100])





