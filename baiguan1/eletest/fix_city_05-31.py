
import pymysql
import pymongo
import grequests
import json

base_api = 'http://api.map.baidu.com/geocoder/v2/?output=json&pois=1&ak=kTLAbkuKsKsu4FpwywNCH62RZnaRMmNb'

conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj', charset='utf8')
# 创建游标
cursor = conn.cursor()

client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,'
    'dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian
db1 = client['Meituan']['lng-lat']

cursor.execute('select poi_id from waimai_poi where source=2 and insert_ts="2017-06-01" and ts_string="2017-05-31"')
ret=cursor.fetchall()
conn.commit()
c=0
urls = []
for poi in ret:
    if c % 10000 == 0:
        print('store_id_num', c)
    c += 1
    poi_id=poi[0]

    doc=database.store_list.find_one({ 'id': poi_id })
    city=doc['city']
    cursor.execute('update waimai_poi set city=%s where poi_id=%s and source=2 and insert_ts=%s',
                   (city, poi_id, '2017-06-01'))
    conn.commit()


    # urls.append(base_api + '&location=' + str(doc['latitude']) + ',' + str(doc['longitude']))
    # if len(urls) >= 10:
    #     rs = (grequests.get(u) for u in urls)
    #     rs = grequests.map(rs)
    #     for i in range(len(rs)):
    #         j = json.loads(rs[i].content.decode())
    #         city = j['result']['addressComponent']['city']
    #         cursor.execute('update waimai_poi set city=%s where poi_id=%s and source=2 and insert_ts=%s',
    #                        (city, poi_id, '2017-06-01'))
    #         conn.commit()
    #     urls = []
    #     ids = []




# def parse(r, docid):
#     j = json.loads(r.content.decode())
# #     print(j)
#     if j['status'] == 0:
# #         print('update', docid, j['result']['addressComponent']['city'])
#         d = db.find_one({ '_id': docid })
#         if d['city'] != j['result']['addressComponent']['city']:
#             try:
#                 print(d['name'], d['city'], d['adname'], j['result']['addressComponent']['city'], j['result']['addressComponent']['district'])
#             except:
#                 print(d, j['result']['addressComponent']['city'], j['result']['addressComponent']['district'])
#         db.update_one(
#             { '_id': docid },
#             { '$set': {
#                 "city": j['result']['addressComponent']['city'],
#                 'adname': j['result']['addressComponent']['district'],
#                 'fixed':1,
#             } }
#         )
#     else:
#         print('FAIL')
#         print(j)
#
# c = 0
# urls = []
# ids = []
# # rr = db.find()
# print('CNT:', rr.count())
# for doc in rr:
#     if c % 100 == 0:
#         print(c)
#     c += 1
#     urls.append(base_api + '&location=' + str(doc['latitude']) + ',' + str(doc['longitude']))
#     if len(urls) >= 10:
#         rs = (grequests.get(u) for u in urls)
#         rs = grequests.map(rs)
#         for i in range(len(rs)):
#             parse(rs[i], ids[i])
#         urls = []
#         ids = []
# print('FIN')