
import os
import random
from pybloom import BloomFilter

def first_num():
    import random
    ran_list = [10, 193, 228, 2227, 5605, 1834]
    for i in range(len(ran_list), 1, -1):
        ran_list[i - 1] = sum(ran_list[:i])

    a = random.randrange(0, ran_list[-1])
    for i in range(len(ran_list)):
        if a < ran_list[i]:
            break
    return str(i+1)

ss = BloomFilter(capacity=10000*10000*15, error_rate=0.0001)
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

    for i in range(5000000):
        if i%10000==0:
            print(path,i)
        while True:
            res = first_num() + "%0.10d" % random.randint(0, 9999999999)
            if res not in ss:
                ss.add(res)
                f.write(res+'\n')
                break
    f.close()
    if i==18:
        break
