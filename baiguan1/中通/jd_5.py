from bo_lib.general.redis_helper import RedisHelper
import sys

r = RedisHelper().client
k=str(sys.argv)
with open('./data/f'+k+'.txt','rb') as f:
    i=0
    j=0
    for line in f:
        i+=1
        if i==50*10000:
            i=0
            j+=1
        r.sadd('jd'+k+'_'+str(j),line.decode().strip())