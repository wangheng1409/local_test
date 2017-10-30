# !/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import defaultdict

oid_list_9=[605,606,607,608,609,650]
ran_list_9 = [51419, 36599, 3124, 784, 142, 11075]
oid_list_12=[210,211,217,220,224,240,250,280,281,310,350,356,605,606,607,608,609,610,630,650,660,667]
ran_list_12=[95,11155,1,1805,1,143,199,5306,1,17,6642,2,22979,16244,1474,336,44,765,26,4962,6,10]
assert len(oid_list_12)==len(ran_list_12)
def first_num(ran_list):
    import random
    for i in range(len(ran_list), 1, -1):
        ran_list[i - 1] = sum(ran_list[:i])

    a = random.randrange(0, ran_list[-1])
    for i in range(len(ran_list)):
        if a < ran_list[i]:
            break
    return i

s=[oid_list_9[first_num(ran_list_9[:])] for i in range(103143)]
# print(s)
s1=[oid_list_12[first_num(ran_list_12[:])] for i in range(72213)]

r1=defaultdict(int)
for i in s:
    r1[str(i)]+=1
r1=sorted(dict(r1).items(),key=lambda x:x[1],reverse=True)
print(r1)

# r2=defaultdict(int)
# for i in s1:
#     r2[str(i)]+=1
# r2=sorted(dict(r2).items(),key=lambda x:x[1],reverse=True)
# print(r2)