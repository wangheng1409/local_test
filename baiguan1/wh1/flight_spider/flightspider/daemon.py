#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = 'fly'

import os
import time

from multiprocessing import Pool
from time import sleep

if __name__ == "__main__":
    start_time = time.time()
    # cmd = "scrapy crawl nsdetail -a task_id=4053  -a ipindex=0 -L INFO"
    cmd = "scrapy crawl bkdetail -a task_id=4358  -L INFO"
    # cmd = "scrapy crawl fudetail -a task_id=4051"
    # cmd = "scrapy crawl fudetail"
    # cmd = "scrapy crawl nsdetail"
    os.system(cmd)
    print time.time() - start_time
