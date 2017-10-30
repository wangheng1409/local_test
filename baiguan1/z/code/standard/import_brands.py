# -*- coding: utf-8 -*-
from lxml import etree
import re
a = open('/data/www/chaomeng-bussiness-tobias/code/standard/brands.html')
tree = etree.HTML(a.read(), parser = etree.HTMLParser(encoding="utf-8"))
out = tree.xpath('//*[@class="colProp-list"]//a')

from standard.models import StandardTag

def brand_names(raw_name):
    toks = name.upper().split(u'（')
    out_name = toks[0].strip()
    brands = out_name.split(u'/')
    if len(brands) == 2:
        return brands[0], brands[1]
    return None, brands[0]

for i in out:
    if i.get('href') == '#':
        continue

    name = i.xpath('normalize-space(text())')
    en_name, cn_name = brand_names(name)
    try:
        if en_name:
            print ' * adding alias: %s' % en_name
            st = StandardTag.objects.get(tag=cn_name)
            st.alias = [en_name]
            st.save()
        else:
            st = StandardTag.objects.get(tag=cn_name)
    except StandardTag.DoesNotExist:
        print ' * adding brand: %s, %s' % (cn_name, en_name)
        if en_name:
            st = StandardTag(tag=cn_name, alias=[en_name], type='brand')
            st.save()
        else:
            st = StandardTag(tag=cn_name, type='brand')
            st.save()