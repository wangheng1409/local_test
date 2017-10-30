import pymongo
import datetime,time
from bo_lib.general import BONotifier

def f():
    client=pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
    database=client.shengjian
    print(str(datetime.date.today()))
    col=database.store_list.find({'ts_string':str(datetime.date.today())},{'id':1})
    col=[x for x in col]
    print(col[0])
    s={}
    c = 0
    for item in col:
        if c % 10000 == 0:
            print('count', c)
        c+=1
        try:
            s[item['id']]=item
        except:
            print(item)

    l=len(list(s.keys()))
    print(l)

    # BONotifier.msg('count(SJ store_id)=%s\n'% (l))
f()