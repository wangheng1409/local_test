# -*- coding: utf-8 -*-
import math
from django.db import connection
from core import sql_utils

def get_prices_category(store_id,start_date,end_date):
   
    sql = """
    SELECT
     (case when sum(num) = 0 then -1 else sum(sales)/sum(num) end) as price_avg ,
      category , item_id
    FROM summary_dailystoreitemsummary
    WHERE
      store_id = '%(store_id)s' AND
      date BETWEEN to_date('%(start_date)s','YYYY-MM-DD') AND to_date('%(end_date)s','YYYY-MM-DD') AND
      sales is not null AND
      num is not null AND
      category is not null
    GROUP BY item_id,category
    """ % {'start_date': start_date, 'end_date': end_date, 'store_id': store_id}
    cur = connection.cursor()
    cur.execute(sql)
    results = sql_utils.dictfetchall(cur)

    out = {}
    for result in results:
        category = result['category']
        price = math.ceil(result['price_avg'])
        if category not in out:
            out[category] = {}
        if price not in out[category]:
            out[category][price] = 0
        out[category][price] += 1 

    return out
        
      
    
