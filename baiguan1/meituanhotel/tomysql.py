import pymongo
import pymysql
import datetime
today=datetime.date.today()

conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj', charset='utf8')
# 创建游标
cursor = conn.cursor()

uri = 'mongodb://root:Baiguan2016@60.205.152.167:3717'
mongo = pymongo.MongoClient(uri)
db1 = mongo['mthotel']['mthotel_detail']
col = db1.find({'cityName':'南昌'}, no_cursor_timeout=True)

c=0
for line in col:
    if c % 1000 == 0:
        print('store_id_num', c)
    c += 1
    try:
        hotel_id=line['poiID']
        hotel_name=line['name']
        hotel_location=line['address']
        hotel_city=line['cityName']
        hotel_score=line['avgScore']
        comment_count=line['commentNum']
        latitude=line['latlng'][0]
        longitude=line['latlng'][1]
        hotel_level=line['hotelStar']
        source=1
        cursor.execute('insert into hotels(hotel_id,hotel_name,hotel_level,hotel_location,hotel_city,hotel_score,comment_count,latitude,longitude,source) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       ( hotel_id,
                         hotel_name,
                         hotel_level,
                         hotel_location,
                         hotel_city,
                         hotel_score,
                         comment_count,
                         latitude,
                         longitude,
                         source
                         ))
        conn.commit()
    except Exception as e:
        print(c, e, '\n', line['_id'] )