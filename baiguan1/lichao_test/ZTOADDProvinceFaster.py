# !/usr/bin/python
# -*-coding: utf-8 -*-
"""
Created on 17/9/8 下午1:54

@author: LiChao
"""
import pymysql
import pandas as pd
import jieba
from concurrent import futures
import gc
from pympler import summary
from pympler import muppy
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

time_test = None


def get_data():
    print('starting...')
    connection = pymysql.connect(host='101.201.120.75',
                                 user='root',
                                 password='baiguandata0808',
                                 db='zto',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    city_sql = """
			select province, city, name from city_list
		"""

    zto_sql = """
			select oid, origin, dest from zto_detail
			where source = 'zto' and origin_province is null
			limit 50000
		"""
    cursor = connection.cursor()
    cursor.execute(city_sql)
    city_pd = pd.DataFrame(cursor.fetchall())
    print(city_pd)

    cursor.execute(zto_sql)
    zto_pd = pd.DataFrame(cursor.fetchall())
    print(zto_pd)

    return connection, city_pd, zto_pd


def main(zto_pd):
    update_sql = 'update zto_detail set origin_province = %s, origin_city = %s, \
                                        dest_province = %s, dest_city = %s where oid = %s'
    special_city = [u'北京市', u'上海市', u'天津市', u'重庆市']
    for index in zto_pd.index:
        oid = zto_pd.loc[index, 'oid']
        origin = zto_pd.loc[index, 'origin'].replace('[', '').replace(']', '').replace(u'地区', '').strip()
        dest = zto_pd.loc[index, 'dest'].replace('[', '').replace(']', '').replace(u'地区', '').strip()

        origin_province = ''
        origin_city = ''
        dest_province = ''
        dest_city = ''
        origin_flag = True
        dest_flag = True
        for i in city_pd.index:
            if origin_flag == False and dest_flag == False:
                break

            if origin_flag:
                if u'市' in origin:
                    if origin in city_pd.loc[i, 'name']:
                        origin_province = city_pd.loc[i, 'province']
                        origin_city = city_pd.loc[i, 'city']
                        origin_flag = False
                else:
                    # origin 不带市的进行切词操作
                    origin_list = list(jieba.cut(origin))
                    for temp in origin_list:
                        if temp in city_pd.loc[i, 'name']:
                            origin_province = city_pd.loc[i, 'province']
                            origin_city = city_pd.loc[i, 'city']
                            origin_flag = False

            if dest_flag:
                if u'市' in dest:
                    if dest in city_pd.loc[i, 'name']:
                        dest_province = city_pd.loc[i, 'province']
                        dest_city = city_pd.loc[i, 'city']
                        dest_flag = False
                else:
                    # dest 不带市的进行切词操作
                    dest_list = list(jieba.cut(dest))
                    for temp in dest_list:
                        if temp in city_pd.loc[i, 'name']:
                            dest_province = city_pd.loc[i, 'province']
                            dest_city = city_pd.loc[i, 'city']
                            dest_flag = False

            if origin_province in special_city:
                origin_city = ''

            if dest_province in special_city:
                dest_city = ''

        connection.cursor().execute(update_sql, (origin_province, origin_city, dest_province, dest_city, oid))
        connection.commit()
        print(index, 'update ok')


def gen_executor(work, slice_list):
    workers = 10
    with ThreadPoolExecutor(workers) as executor:
        futures = [executor.submit(work, slice_item) for slice_item in slice_list]
        for future in as_completed(futures):
            futures.remove(future)
            yield


if __name__ == '__main__':
    connection, city_pd, zto_pd = get_data()

    slice_list = []  # 切成功后的 ：[[],[],[],[]]
    _slice = 1000
    for i in range(len(zto_pd) // _slice):
        a = zto_pd[:_slice]
        del zto_pd[:_slice]
        slice_list.append(a)
    zto_list = len(slice_list) * 1000
    print('slice_list ok', zto_list)

    # zto_list = list()
    # split_num = 10000
    # total = len(zto_pd) // split_num + 1
    # count = 0
    # for index in range(total):
    #     temp_zto = zto_pd.loc[ count * split_num : (count+1) * split_num - 1 ]
    #     count += 1
    #     zto_list.append(temp_zto)
    # print(len(zto_list))

    # main(zto_pd)

# workers = 6
# with futures.ThreadPoolExecutor(workers) as executor:
# 	res = executor.map(main, zto_list)

# 新的方法
    for cycle in gen_executor(main, zto_list):
        gc.collect()
    # connection.close()
