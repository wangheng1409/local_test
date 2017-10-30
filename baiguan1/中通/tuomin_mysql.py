# !/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import pymysql
import hashlib
def md5(password):
    hash = hashlib.md5()
    hash.update(bytes(password, encoding='utf-8'))
    return hash.hexdigest()

# 创建连接
conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='zto', charset='utf8')
# 创建游标
cursor = conn.cursor()

md5_str='as789df7i3m*&$*#UND*+_)'

regx_list=[
    'tel="(\d+-\d+)',
     'mobile=(\d+)',
    '13[0-9]{9}|15[012356789][0-9]{8}|18[0-9]{9}|14[579][0-9]{8}|17[0-9]{9}',
    '的(.{1,20})已收件',
    '的(.{1,20})正在',
    '签收人:(.{1,20}),',
           ]

cursor.execute("select `oid`,`raw` from zto_detail limit 1")
ret=cursor.fetchall()
for item in ret:
    oid=item[0]
    raw=item[1]
    for reg in regx_list:
        a=re.findall(reg,raw)
        b=[x for x in a if x]
        for st in b:
            md5_st=md5(st+md5_str)
            raw=raw.replace(st,md5_st)
    print(raw)




