# -*- coding: utf-8 -*-

import sys
from datahub import DataHub
from datahub.models import RecordType, TupleRecord
from pymongo import MongoClient
from bson import ObjectId
import threading
import Queue
import time

# uri = 'mongodb://root:Baiguan2016@60.205.152.167:3717'
uri = 'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521'
mongo = MongoClient(uri)
db = mongo['shengjian']['store_menu_list']
access_id = 'LTAIypzOElY3tnVG'
access_key = 'kxR8s0VfwCzuh7atsLt3DEAqe5tnuf'
endpoint = 'http://dh-cn-hangzhou.aliyuncs.com'
dh = DataHub(access_id, access_key, endpoint)
project_name = 'kysj_2mc'
topic_name = 'sj_menu'


