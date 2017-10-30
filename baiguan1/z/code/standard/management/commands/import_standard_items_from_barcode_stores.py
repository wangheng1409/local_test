from django.core.management.base import BaseCommand
from standard.models import StandardItem
from django.conf import settings
import preprocessing
import psycopg2
import datetime
class Command(BaseCommand):
    """
        we have a list of stores that provide barcodes and items items.
        This data will be used to build up the standard db
    """
    help = 'Usage: python manage.py sync_standard_items'

    def load_from_trade_db(self):
        conn = psycopg2.connect(host=settings.TRADE_DB_HOST, \
                                port=settings.TRADE_DB_PORT, \
                            database=settings.TRADE_DB_NAME, \
                                user=settings.TRADE_DB_USERNAME, \
                            password=settings.TRADE_DB_PASSWORD,
                            sslmode='require')

        cur = conn.cursor()
        cur.execute(
            """
            SELECT item_id, item_name, price, device_id from trade_trade where item_id like '69%' and length(item_id) = 13;
            """)
        result =  cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return result

    def __store_prices(self, store_prices):
        all_item_prices = {}
        for t in store_prices:
            all_item_prices[t[0]] = t[1]
        return all_item_prices

    def __store_prices_to_list(self, all_prices):
        out = []
        for k,p in all_prices.items():
            out.append([k,p])
        return out

    def handle(self, *args, **options):
        items = self.load_from_trade_db()
        total = float(len(items))
        print 'Total: %d' % total
        i = 0
        for k in items:
            i += 1
            barcode = k[0][:13]
            item_name = k[1]
            price = k[2]
            device_id = k[3]
            out = '  %.2f) * Processing Item %s |||| %s' % (round(i/total*100.0, 2), barcode, item_name)
            print out.encode('utf-8')
            if len(item_name) > 0:
                try:
                    si = StandardItem.objects.get(barcode=barcode)
                    should_save = False
                    if si.alias:
                        if item_name not in si.alias:
                            alias_list = si.alias
                            alias_list.append(item_name)
                            si.alias = alias_list
                            should_save = True
                    else:
                        si.alias = [item_name]
                        should_save = True

                    if si.store_prices:
                        all_item_prices = self.__store_prices(si.store_prices)
                        if device_id not in all_item_prices:
                            all_item_prices[device_id] = price
                            si.store_prices = self.__store_prices_to_list(all_item_prices)
                            should_save = True
                    else:
                        si.store_prices = [[device_id, price]]
                        should_save = True

                    if should_save:
                        si.save()

                except StandardItem.DoesNotExist:
                    t_dict = preprocessing.models.Item(item_name)
                    si = StandardItem(barcode=barcode[:13], \
                                      name=t_dict.name, \
                                      flavor=t_dict.flavor, \
                                      model=t_dict.model, \
                                      keywords=t_dict.keywords, \
                                      status='new', \
                                      alias=[item_name], \
                                      store_prices=[[device_id, price]])
                    si.save()
        print datetime.datetime.now()

