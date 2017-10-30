
import pymysql
import datetime
today=datetime.date.today()

conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj', charset='utf8')
# 创建游标
cursor = conn.cursor()

c=0
with open('a.txt','r') as f:
    for line in f:
        if c % 1000 == 0:
            print('store_id_num', c)
        c+=1
        try:
            s=line.split(',')
            ky_id=s[0]
            ky_name=s[1]
            ky_phone=s[2]
            sj_id=s[3]
            sj_name=s[4]
            sj_phone=s[5]
            distince=s[6]
            cursor.execute('insert into overlap_poi(ky_id,ky_name,ky_phone,sj_id,sj_name,sj_phone,distince,insert_ts) values(%s,%s,%s,%s,%s,%s,%s,%s)',
                           ( ky_id,
                             ky_name,
                             ky_phone,
                             sj_id,
                             sj_name,
                             sj_phone,
                             distince,
                             str(today)
                             ))
            conn.commit()
        except Exception as e:
            print(c,e,'\n',line,)