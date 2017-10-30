import datetime, time
import pymysql
import pymongo

conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj', charset='utf8')
# 创建游标
cursor = conn.cursor()

client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian
db1 = client['Meituan']['lng-lat']

cursor.execute('select poi_id from waimai_poi where source=2 and insert_ts="2017-06-01" and month_sale is null ')
ret=cursor.fetchall()
conn.commit()
c=0
for poi in ret:
    if c % 1000 == 0:
        print('store_id_num', c)
        if c>1:
            conn.commit()
    c += 1
    poi_id=poi[0]
    if database.store_list.find_one({ 'id': poi_id ,'ts_string':{'$gte':'2017-06-01'}}):
        item=database.store_list.find_one({ 'id': poi_id ,'ts_string':{'$gte':'2017-06-01'}})
        month_sale = item.get('recent_order_num', 0)
        cursor.execute('update waimai_poi set month_sale=%s where poi_id=%s and source=2 and insert_ts=%s', (month_sale, poi_id,'2017-06-01'))
conn.commit()
