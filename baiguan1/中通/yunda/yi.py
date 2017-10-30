# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import random
from pybloom import BloomFilter

ss = BloomFilter(capacity=10000*10000*15, error_rate=0.0001)
base_path='./yunda_data/'
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
    path='./yunda_data/f'+k+'.txt'
    if os.path.exists(path):
        continue

    f=open(path,'w')

    for j in range(1000000):
        if j%10000==0:
            print(path,j)
        while True:
            res = random.choice(['1','3','9']) + "%0.12d" % random.randint(0, 999999999999)
            if res not in ss:
                ss.add(res)
                f.write(res+'\n')
                break
    f.close()
    if i==50:
        break
