# -*- coding: utf-8 -*-
from django.db import connection
from core import sql_utils
import datetime

def get_basket_coefficient(store_id,start_date,end_date):
    sql = '''
    SELECT 
      count(sd.id) as count_id,sum(sd.num) as sum_num, sum(sd.sales) as sum_sales ,ss.name ,sd.category, 
      sum(sd.num)/count(sd.id) as basket,sum(sd.sales)/sum(sd.num) as price_avg 
    FROM 
      summary_dailystoreitemsummary as sd,store_storeitem as ss 
    WHERE
      sd.date BETWEEN to_date('%(start_date)s','YYYY-MM-DD') AND to_date('%(end_date)s','YYYY-MM-DD') AND
      sd.store_id = '%(store_id)s' AND
      sd.item_id = ss.id AND
      category is not null 
    GROUP BY sd.item_id,ss.name,category
    ORDER BY category,basket; 
    ''' % {'start_date':start_date,'end_date':end_date,'store_id':store_id}
    cur = connection.cursor()
    cur.execute(sql)
    results = sql_utils.dictfetchall(cur)
    return results         

def get_basket_week(store_id):
    start_date = (datetime.date.today() - datetime.timedelta(days=70)).strftime('%Y-%m-%d')
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    sql = '''
    SELECT
      count(sd.id) as count_id,sum(sd.num) as sum_num,to_char(sd.date,'YYYY-MM-DD') as date
    FROM
      summary_dailystoreitemsummary as sd
    WHERE
      sd.date BETWEEN to_date('%(start_date)s','YYYY-MM-DD') AND to_date('%(end_date)s','YYYY-MM-DD') AND
      store_id = '%(store_id)s'
    GROUP BY date 
    ''' % {'start_date':start_date,'end_date':end_date,'store_id':store_id}
    cur = connection.cursor()
    cur.execute(sql)
    results = sql_utils.dictfetchall(cur)
    week_results = {}
    for result in results:
        myDate = result['date']
        sum_num = result['sum_num']
        count_id = result['count_id']
        week = datetime.datetime.strptime(myDate, "%Y-%m-%d").weekday()
        if week not in week_results:
            week_results[week] = {'sum':0.0,'count':0.0}
        week_results[week]['sum'] += sum_num
        week_results[week]['count'] += count_id
    for week,week_result in week_results.items():
        week_results[week]['basket'] = week_results[week]['sum']/week_results[week]['count']
    return week_results

def get_basket_salesper(store_id,start_date,end_date):
    sql = '''
    SELECT
     (case when sales_all.sum_sales_all = 0 then 0 else (sales_top.sum_sales_top+0.0)/sales_all.sum_sales_all end ) as sales_per,
      basket,sales_top.date_out as out_date 
    FROM
    (
     (SELECT
        sum(sd.sales) as sum_sales_top,to_char(sd.date,'YYYY-MM-DD') as date_out,sum(sd.num)/count(sd.id) as basket
      FROM 
        (
        SELECT
          sum(sales) as sum_sales,item_id 
        FROM
          summary_dailystoreitemsummary  
        WHERE
          date BETWEEN to_date('%(start_date)s','YYYY-MM-DD') AND to_date('%(end_date)s','YYYY-MM-DD')  AND
          store_id = '%(store_id)s' 
        GROUP BY item_id 
        ORDER BY sum_sales desc limit 20
        ) as top,
        summary_dailystoreitemsummary as sd
      WHERE
        sd.item_id = top.item_id
      GROUP BY date_out
      ) as  sales_top
      JOIN 
        (
        SELECT
          sum(sales) as sum_sales_all,to_char(date,'YYYY-MM-DD') as my_date 
        FROM summary_dailystoreitemsummary 
        WHERE
          date BETWEEN to_date('%(start_date)s','YYYY-MM-DD') AND to_date('%(end_date)s','YYYY-MM-DD')  AND
          store_id = '%(store_id)s' group by my_date
        )sales_all
      ON
        sales_top.date_out = sales_all.my_date
    ) 
    ORDER BY
      sales_top.date_out;
    ''' % {'start_date':start_date,'end_date':end_date,'store_id':store_id}
    cur = connection.cursor()
    cur.execute(sql)
    results = sql_utils.dictfetchall(cur)
    return results         
