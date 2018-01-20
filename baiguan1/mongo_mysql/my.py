# !/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
import pandas as pd
from sqlalchemy import create_engine
import datetime
import pymysql
pymysql.install_as_MySQLdb()

def create_new_with_limit(db_name, column_delete, insert_ts):
    print 'starting...'
    host = '123.59.69.66'
    port = 5600
    user = 'root'
    password = 'big_one_112358'
    url = 'mongodb://' + user + ':' + password + '@' + host + ':' + str(port) + '/'
    client = MongoClient(url)
    db = client.lifefood
    collection = db[db_name]
    select_condition = {'_id': 0}
    if len(column_delete) > 0:
        for temp in column_delete:
            select_condition[ temp] = 0
    print select_condition

    total = collection.find({'ts_string': '2017-11-23'}, select_condition).count()
    print total
    every_time = 10000
    for i in range(0, total / every_time + 1):
        print i
        skip_number = i * every_time
        # collection_pd = pd.DataFrame(list(collection.find({}, select_condition).limit(every_time).skip(skip_number)))
        collection_pd = pd.DataFrame(list(collection.find({'ts_string': '2017-11-23'}, select_condition).limit(every_time).skip(skip_number)))

        print collection_pd.info()

        # 对特殊字段进行处理, 如数组类型、字典类型
        # ziru 中 bizcircle_name 有数组类型, 需要转成字符串
        if 'bizcircle_name' in collection_pd.columns:
            collection_pd['bizcircle_name'] = collection_pd['bizcircle_name'].map(lambda x: ','.join(x) if type(x) == list else x)

        # mogu 中 rentType 字段是字典类型, 需要截取出 value 值
        if 'rentType' and 'image' in collection_pd.columns:
            collection_pd['rentType'] = collection_pd['rentType'].map(lambda x: x['value'])

        collection_pd['insert_ts'] = pd.Series([insert_ts] * len(collection_pd))
        insert_to_mysql(collection_pd, db_name)
    client.close()


def insert_to_mysql(temp_pd, table_name):
    host = '101.201.120.75:3306'
    user = 'root'
    password = 'baiguandata0808'
    db = 'lifefood'
    mysql_url = 'mysql+mysqldb://' + user + ':' + password + '@' + host + '/' + db + '?charset=utf8'
    engine = create_engine(mysql_url, echo=True)
    temp_pd.to_sql(name = table_name, con=engine, flavor=None, index=False, if_exists='append')


def main(insert_ts):
    # lianjia
    # db_name, column_delete = 'storelist_wap_detail', ['recommendReasonData',
    #                                                   'adInfo',
    #                                                   'shopDealInfos',
    #                                                   'shopPositionInfo',
    #                                                   'tagList',
    #                                                   'shopStateInformation',
    #                                                   'defaultPic',
    #                                                   'dishtags',
    #                                                   'originalUrlKey',
    #                                                   'recommendReason',
    #                                                   ]
    db_name, column_delete = 'review_all1_detail', []

    create_new_with_limit(db_name, column_delete, insert_ts)



if __name__ == '__main__':
    today = datetime.datetime.now()
    insert_ts = today.strftime('%Y-%m-%d')
    main(insert_ts)