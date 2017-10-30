from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

import datetime
import pandas
from sqlalchemy import create_engine
import sqlalchemy as sa

'''
1. load store sku from data server
2. find the new sku
3. add the new sku to db
'''
class Command(BaseCommand):
    help = 'Usage: python manage.py import_store_items store_id'

    def handle(self, *args, **options):
        print args
        print options
        # data_engine = create_engine(settings.TRADE_DB_URL)
        # all_rows = pandas.read_sql_query(
        #     """
        #     SELECT distinct on(trade_trade.item_name)
        #         trade_devicestore.store_id,
        #         item_name as name,
        #         price,
        #         item_id as receipt_item_id,
        #         lag(traded_at, 0) over (partition by item_name order by traded_at asc) as trade_at
        #     from trade_trade
        #     join trade_devicestore
        #     on trade_devicestore.device_id = trade_trade.device_id
        #     where trade_devicestore.store_id=%(store_id)s;
        #     """, data_engine, params={'store_id': '440'})

        # bussiness_engine = create_engine(settings.BUSSINESS_DB_URL)
        # new_row_ids = pandas.read_sql_query(sa.text(
        #     """
        #         SELECT unnest(array[:names]) as name
        #         except
        #         SELECT name from store_storeitem where store_id=:store_id group by name
        #     """),
        #     bussiness_engine,
        #     params={'names': all_rows['name'].tolist(), 'store_id':all_rows.values[0][0]})


        # new_rows = pandas.merge(all_rows, new_row_ids, how='inner', on=['name'])

        # new_rows['last_updated'] = pandas.to_datetime(timezone.now())
        # new_rows['trade_at'] = new_rows['trade_at'].astype('object')
        # new_rows['status'] = 'new'
        # new_rows.to_sql('store_storeitem', bussiness_engine, if_exists='append', index=False)

        # print '   Added %d new items' % new_rows.count()[0]
