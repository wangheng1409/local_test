from django.core.management.base import BaseCommand
from django.db import connection
from store.models import StoreItem
import datetime

class Command(BaseCommand):
    help = 'Usage: python manage.py verify_store_item_data'

    def handle(self, *args, **options):
        si = StoreItem.objects.exclude(standard_item__isnull=True)
        # si = si[:10]
        total = float(si.count())
        i = 0
        for s in si:
            i += 1
            print '  %.2f) * Processing Item %s |||| %s' % (round(i/total*100.0, 2), s.id, s.name)
            standard = s.standard_item
            if standard.mean and standard.std_dev >= 0:
                if (s.price < standard.mean - 2 * standard.std_dev or \
                          s.price > standard.mean + 2 * standard.std_dev):
                    # print 'out of range...'
                    # print standard.mean
                    # print standard.std_dev
                    # print s.price
                    # print 'left: %f' % (standard.mean - 2 * standard.std_dev)
                    # print 'right: %f' % (standard.mean + 2 * standard.std_dev)
                    s.status = 'error'
                    s.save()

