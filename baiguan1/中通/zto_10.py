from bo_lib.general.redis_helper import RedisHelper

r = RedisHelper().client
k=str(14)
with open('./data/f'+k+'.txt','rb') as f:
    i=0
    j=0
    for line in f:
        i+=1
        if i==100*10000:
            i=0
            j+=1
        r.sadd('z'+k+'_'+str(j),line.decode().strip())