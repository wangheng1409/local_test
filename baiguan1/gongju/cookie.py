# !/usr/bin/env python
# -*- coding:utf-8 -*-

s='_snstyxuid=ADA6E7420047O2QN; cityId=9265; provinceCode=230; cityCode=028; cityName=%E6%88%90%E9%83%BD; city=1000268; province=230; district=10002681; _snmc=1; _snsr=direct%7Cdirect%7C%7C%7C; _snma=1%7C150676122876861599%7C1506761228768%7C1506761228768%7C1506761228768%7C1%7C1; _snmp=150676122746316220; _snmb=150676122877461174%7C1506761228785%7C1506761228775%7C1; _snms=150676122878650858'
s=s.split(';')
w={}
for item in s:
    k,v=item.split('=')
    w[k]=v
print(w)