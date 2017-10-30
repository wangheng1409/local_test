# -*- coding: utf-8 -*-

from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def __category_names_to_ids(names):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT array_agg(id) as categories from standard_category where (%s)
    """ % ' or '.join(["name='%s'" % n for n in names]))
    result = dictfetchall(cursor)
    return result[0]['categories']

def __extract_operator(key):
    toks = key.split('__')
    if len(toks) == 2:
        return toks[0], toks[1]
    return key, None

def __convert_to_sql(k, v):
    if v['splitter'] == 'or':
        sub = []
        if k == 'category_id':
            v['value'] = __category_names_to_ids(v['value'])

        for i in v['value']:
            sub.append("%s='%s'" % (k, i))
        return '(%s)' % ' or '.join(sub)
    elif v['splitter'] == 'between':
        return "(%s between '%s' and '%s')" % (k, v['value'][0], v['value'][1])

def __strip_each(l):
    return [val.strip() for val in l]

def growth_rate(rate):
    if rate:
        return '+%.2f' % rate if rate > 0 else '%.2f' % rate

def query_builder(q, m):
    toks = q.split('@')
    d = {}
    for t in toks:
        kv = t.strip().split('=')
        if len(kv) != 2:
            continue
        key = kv[0].strip()
        key, opeartor = __extract_operator(key)
        if key in m:
            if opeartor and opeartor == u'在':
                values = kv[1].split('~')
                if len(values) != 2:
                    continue
                d[m[key]] = {'splitter': 'between', 'value': __strip_each(values)}
            else:
                d[m[key]] = {'splitter': 'or', 'value': __strip_each(kv[1].split(','))}

    out = []
    for key, values in d.items():
        out.append(__convert_to_sql(key, values))
    return ' and '.join(out)
