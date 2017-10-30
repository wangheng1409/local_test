from django.core.management.base import BaseCommand
from standard.models import StandardItem
from django.db.models import Q
from preprocessing import constants, models

class Command(BaseCommand):
    help = 'Usage: python manage.py extract_flavors'

    def handle(self, *args, **options):
        items = StandardItem.objects.all()
        count = 0
        for i in items.all():
            pitem = models.Item(i.name)
            i.flavor = pitem.flavor
            i.save()
            # print i.name, pitem.flavor
            # count += 1
            # if count > 100:
            #     break