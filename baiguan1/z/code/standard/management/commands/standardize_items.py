from django.core.management.base import BaseCommand
from standard.models import StandardItem
from store.models import StoreItem
from django.db.models import Q
from preprocessing.utils import rank_standard_items, find_ranking_candidates
import preprocessing

class Command(BaseCommand):
    help = 'Usage: python manage.py standardize_items'

    def handle(self, *args, **options):
        items = StoreItem.objects.filter(Q(status='pending_review') | Q(status='new'))
        # items = StoreItem.objects.filter(receipt_item_id = '6921168593576')

        total = float(items.count())
        print 'Total: %d' % total
        i = 0
        auto_matches = 0
        pending_review = 0
        for k in items:
            i += 1
            d = k.to_dict()
            candidates = find_ranking_candidates(d['name'])
            receipt_barcode = d['receipt_item_id']
            print '  %.2f) * Processing Item %s |||| %s' % (round(i/total*100.0, 2), d['id'], d['name'])
            if receipt_barcode and len(receipt_barcode) > 10:
                try:
                    standard_item_from_receipt = StandardItem.objects.get(barcode=receipt_barcode)
                    if standard_item_from_receipt.alias:
                        if d['name'] not in standard_item_from_receipt.alias:
                            alias_list = standard_item_from_receipt.alias
                            alias_list.append(d['name'])
                            standard_item_from_receipt.alias = alias_list
                            standard_item_from_receipt.save()
                    else:
                        standard_item_from_receipt.alias = [d['name']]
                        standard_item_from_receipt.save()

                except StandardItem.DoesNotExist:
                    t_dict = preprocessing.models.Item(d['name'])
                    standard_item_from_receipt = StandardItem(barcode=receipt_barcode, name=t_dict.name, flavor=t_dict.flavor, model=t_dict.model, keywords=t_dict.keywords, status='pending_review', alias=[d['name']])
                    standard_item_from_receipt.save()
                k.standard_item = standard_item_from_receipt
                k.status = 'auto_verified'
                auto_matches += 1
                k.save()
            else:
                ranked_candidates_ids, scores = rank_standard_items(candidates, d)
                if len(ranked_candidates_ids) > 0:
                    k.candidates = ranked_candidates_ids
                    k.candidates_scores = scores
                    k.standard_item = StandardItem.objects.get(pk=ranked_candidates_ids[0])

                    if scores[0] > 0.81:
                        k.status = 'auto_verified'
                        auto_matches += 1
                    else:
                        k.status = 'pending_review'
                        pending_review += 1
                    k.save()
                print '  No matches'

        print '# of Auto mathces: %d' % auto_matches
        print '# of Pending review: %d' % pending_review