from django.core.management.base import BaseCommand
from standard.models import StandardItem
from django.conf import settings
import numpy as np

class Command(BaseCommand):
    """
        Compute standard items mean, std
    """
    help = 'Usage: python manage.py compute_stats'

    def remove_outliers(self, prices):
        mid = np.percentile(prices, 50)
        q1 = np.percentile(prices, 25)
        q3 = np.percentile(prices, 75)
        k = (q3 - q1) * 1.5
        right = q3 + k
        left = q1 - k

        out = []
        for p in prices:
            if p <= right and p >= left:
                out.append(p)
        return out

    def handle(self, *args, **options):
        items = StandardItem.objects.exclude(store_prices__isnull=True)
        total = float(len(items))
        print 'Total: %d' % total

        i = 0
        for s in items.all():
            i += 1
            print '  %.2f) * Processing Item %s |||| %s' % (round(i/total*100.0, 2), s.barcode, s.name)
            if len(s.store_prices) > 3:
                print '   **'
                prices = [float(p[1]) for p in s.store_prices]
                clean_prices = self.remove_outliers(prices)
                if len(clean_prices) > 1:
                    mean = round(np.mean(clean_prices), 2)
                    std = round(np.std(clean_prices), 2)
                    s.mean = mean
                    s.std_dev = std
                    s.save()


