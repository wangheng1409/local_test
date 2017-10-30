import os
import random
from pybloom import BloomFilter

ss=BloomFilter(capacity=1000*100000000, error_rate=0.001)
base_path='./data/'
name_list=os.listdir(base_path)
for file in name_list:
    path=base_path+file

    with open(path,'r') as f:
        c=0
        for line in f:
            if c%10000==0:
                print('ss_add', path,c)
            c+=1
            ss.add(line.strip())

for i in range(100):
    k=str(i)
    path='./data/f'+k+'.txt'
    if os.path.exists(path):
        continue
    f=open(path,'w')

    for i in range(10000000):
        if i%10000==0:
            print(path,i)
        while True:
            res = random.choice(['4', '7', '5']) + "%0.11d" % random.randint(0, 99999999999)
            if res not in ss:
                f.write(res+'\n')
                break
    f.close()
    break


import redis

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
r = redis.Redis(connection_pool=pool)
k=str(0)
with open('f'+k+'.txt','rb') as f:
    for line in f:
        r.sadd('z0',line.decode().strip())


