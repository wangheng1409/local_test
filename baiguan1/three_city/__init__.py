import pandas as pd
import json
import pymongo
import requests
from lxml import html
from lxml import etree
import time
import datetime
f=open('5&_skc=800.html','r',encoding='utf8')
s=''.join(f.readlines())

response=html.fromstring(s)
table=response.xpath('//li[starts-with(@id,"item")]')
print(len(table))