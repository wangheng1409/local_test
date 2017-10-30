import datetime, time
import pymysql
import pymongo

conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj', charset='utf8')
# 创建游标
cursor = conn.cursor()

client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@60.205.152.167:3717')
database = client.shengjian
db1 = client['Meituan']['lng_lat_short']

cursor.execute(
    "select poi_id,name from (select poi_id,city,ts_string, poi_address, substr(poi_address,1,3) as name from waimai_poi where insert_ts = '2017-06-13' and source = 2 and ts_string > '2017-06-05' ) t  where city != name and name like '%市'")
ret = cursor.fetchall()
conn.commit()
c = 0
for poi in ret:
    if c % 1000 == 0:
        print('store_id_num', c)
        if c > 1:
            conn.commit()
    c += 1
    poi_id = poi[0]
    name = poi[1]

    try:
        cursor.execute('update waimai_poi set city=%s where poi_id=%s and source=2 and insert_ts=%s',
                       (name, poi_id, '2017-06-13'))

    # print(c)
    except:
        pass
conn.commit()