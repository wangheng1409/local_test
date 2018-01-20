
# !/usr/bin/env python
# -*- coding:utf-8 -*-
import requests


ret=requests.get('http://www.kuaidaili.com/free/inha/1').text
print(ret)