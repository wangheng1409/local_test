from django.core.management.base import BaseCommand
from django.db import connection
from store.models import StoreItem
import datetime

class Command(BaseCommand):
    help = 'Usage: python manage.py verify_store_item_data'

    def handle(self, *args, **options):
        si = StoreItem.objects.exclude(standard_item__isnull=True)
        si = si[:5]
        for s in si:
            standard = si.standard_item
            if s.price < standard.mean - 2*standard.std_dev or s.price > standard.mean + 2*standard.std_dev:
                print 'out of range...'
                print s.price
                print 'left: %f' % standard.mean - 2*standard.std_dev
                print 'right: %f' % standard.mean + 2*standard.std_dev

