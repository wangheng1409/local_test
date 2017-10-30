
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
r = redis.Redis(connection_pool=pool)
k=str(0)
with open('./baishi_data_12/f'+k+'.txt','rb') as f:
    for line in f:
        r.sadd('baishi_12_'+k,line.decode().strip())