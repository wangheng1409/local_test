#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = 'fly'

import time

from cleardata import clear_overdue_flight

if __name__ == "__main__":
    while True:
        start_time = time.time()
        clear_overdue_flight()
        print "clear done consuming time %s second." % str(time.time() - start_time)
        time.sleep(60)
