# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import random
from pybloom import BloomFilter
oid_list_9=[605,606,607,608,609,650]
ran_list_9 = [51419, 36599, 3124, 784, 142, 11075]
oid_list_12=[210,211,217,220,224,240,250,280,281,310,350,356,605,606,607,608,609,610,630,650,660,667]
ran_list_12=[95,11155,1,1805,1,143,199,5306,1,17,6642,2,22979,16244,1474,336,44,765,26,4962,6,10]
def first_num(ran_list):
    import random
    for i in range(len(ran_list), 1, -1):
        ran_list[i - 1] = sum(ran_list[:i])

    a = random.randrange(0, ran_list[-1])
    for i in range(len(ran_list)):
        if a < ran_list[i]:
            break
    return i

ss = BloomFilter(capacity=10000*10000*15, error_rate=0.0001)
base_path='./baishi_data_12/'
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
    path='./baishi_data_12/f'+k+'.txt'
    if os.path.exists(path):
        continue

    f=open(path,'w')

    for j in range(1000000):
        if j%10000==0:
            print(path,j)
        while True:
            res = str(oid_list_12[first_num(ran_list_12[:])]) + "%0.9d" % random.randint(0, 999999999)
            if res not in ss:
                ss.add(res)
                f.write(res+'\n')
                break
    f.close()
    if i==50:
        break
