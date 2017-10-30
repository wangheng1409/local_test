import redis

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
r = redis.Redis(connection_pool=pool)
k=str(13)
with open('./data/f'+k+'.txt','rb') as f:
    i=0
    j=0
    for line in f:
        i+=1
        if i==100*10000:
            i=0
            j+=1
        r.sadd('jd'+k+'_'+str(j),line.decode().strip())