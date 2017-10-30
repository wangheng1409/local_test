# !/usr/bin/python
# -*-coding: utf-8 -*-
"""
Created on 17/6/13 下午5:52

@author: LiChao
"""
from pymongo import MongoClient
import pandas as pd
from sqlalchemy import create_engine
from datetime import *

def main():
    print 'starting...'
    host = '60.205.152.167'
    port = 3717
    user = 'root'
    password = 'Baiguan2016'
    url = 'mongodb://' + user + ':' + password + '@' + host + ':' + str(port) + '/'
    client = MongoClient(url)
    db = client.stock
    s=list(db.holdings.find({}, {'_id': 0}))

    print len(s)
    host = '101.201.120.75'
    user = 'root'
    password = 'baiguandata0808'
    db = 'intime'
    mysql_url = 'mysql+mysqldb://' + user + ':' + password + '@' + host + '/' + db + '?charset=utf8'
    engine = create_engine(mysql_url, echo=True)
    while s:
        t=s[:10000]
        del s[:10000]
        stock_detail_pd = pd.DataFrame(t)
        stock_detail_length = len(stock_detail_pd)
        print stock_detail_length

        stock_detail_pd['insert_ts'] = pd.Series([datetime.now().strftime('%Y-%m-%d')] * stock_detail_length)
        print stock_detail_pd.info()
        print len(stock_detail_pd)
        stock_detail_pd.to_sql(name='holdings', con=engine, flavor=None, if_exists='append', index=False)

if __name__ == '__main__':
    main()