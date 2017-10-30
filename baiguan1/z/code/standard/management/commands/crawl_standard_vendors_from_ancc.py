from django.core.management.base import BaseCommand
from standard.models import StandardVendor
from django.conf import settings
from django.db.models import Q
import preprocessing
import requests
import lxml.html
from lxml import etree
import datetime

class Command(BaseCommand):
    """
        we have a list of stores that provide barcodes and items items.
        This data will be used to build up the standard db
    """
    help = 'Usage: python manage.py sync_standard_vendors'

    def load_sv_name(self, barcode):
        url = 'http://search.anccnet.com/searchResult2.aspx'
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'


        cookies = {
            'ASP.NET_SessionId': 'gr0er545is1f3f5514ytpt55',
            'ASP.NET_SessionId_NS_Sig': 'oenCV6mdznwg-VC_',
        }

        headers = {
            'Origin': 'http://www.ancc.org.cn',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Referer': 'http://www.ancc.org.cn/Service/queryTools/internal.aspx',
            'Connection': 'keep-alive',
        }

        data = '__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTE5NTYxNDQyMTkPZBYCAgEPZBYCAhMPFgIeB1Zpc2libGVnFgYCAQ8PFgIeBFRleHQFCDY5MDMxNDgxZGQCAw8PFgIfAGhkZAIFD2QWAgIDDw8WAh4LUmVjb3JkY291bnQCAWRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYFBRJSYWRpb0l0ZW1Pd25lcnNoaXAFDVJhZGlvSXRlbUluZm8FBlJhZGlvMQUGUmFkaW8yBQZSYWRpbzOGBSruQoGLASsEf3dNgHe7Lv4yKw%3D%3D&__EVENTVALIDATION=%2FwEWCgLDl%2FrsBALLnru%2FBwKB7J3yDAKbg6TuCQLj%2BszOBgLC79P5DgLC78f5DgLC78v5DgLChPy%2BDQLjwOP9CPxkjrTyxPitXCxg%2BTYMC27IPRoN&Top%24h_keyword=&query-condition=RadioItemOwnership&query-supplier-condition=Radio1&txtcode={0}&btn_query=%E6%9F%A5%E8%AF%A2+'.format(barcode)

        r = requests.post('http://www.ancc.org.cn/Service/queryTools/internal.aspx', headers=headers, cookies=cookies, data=data)

        tree = lxml.html.fromstring(r.text)
        out = tree.xpath('normalize-space(//*[@id="searchResult"]/div/table/tbody/tr/td[2])')
        return out

    def handle(self, *args, **options):
        print self.load_sv_name('69592034')
        # sv = StandardVendor.objects.filter(Q(name__isnull=True) | Q(status='new'))
        # total = float(sv.count())
        # count  = 0
        # print datetime.datetime.now()
        # for s in sv:
        #     count += 1
        #     print '  %.2f Processing %s' % ((count/total)*100.0, s.barcode)
        #     s.status = 'pending_review'
        #     sv_name = self.load_sv_name(s.barcode)
        #     s.name = sv_name
        #     s.save()
        # print datetime.datetime.now()