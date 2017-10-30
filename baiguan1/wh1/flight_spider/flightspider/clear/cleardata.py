#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = 'fly'

import time
from flightspider import database


def clear_overdue_flight():
    sys_config = database.db.query("select * from sys_config where ctype=1")
    for sc in sys_config:
        limit = 50
        offset = 0
        while True:
            sel_sql = "SELECT * FROM flight_detail WHERE syncTime < date_add(now(), interval -(syncCycle+%s) MINUTE)" \
                      " AND company=%s LIMIT %s OFFSET %s"
            flight_list = database.db.query(sel_sql, sc["cvalue"], sc["cname"], limit, offset)
            print flight_list
            offset += limit
            if not len(flight_list):
                break
            fileds = ["company", "flightNo", "flightDate", "cabinId", "depCode", "arrCode", "price", "vipPrice",
                      "priceCurrency", "surplusTicket", "share", "remarks"]
            col = ",".join(fileds)
            col2 = ",".join(["%s" for f in fileds])
            insert_sql = "insert into flight_detail_history("+col+") values ("+col2+");"
            ids = []
            insert_params = []
            for cfd in flight_list:
                insert_params.append([cfd[f] for f in fileds])
                ids.append(str(cfd['id']))
            try:
                database.db.insertmany(insert_sql, insert_params)
            except:
                pass
            ids_str = ",".join(ids)
            database.db.execute("delete from flight_detail where id in (%s);" % ids_str)


if __name__ == "__main__":
    clear_overdue_flight()

