from os import environ

import pandas
import sqlalchemy
import datetime
import collections
import redis

def extract_tags(store_id):
    bussiness_engine = sqlalchemy.create_engine(environ.get('CM_BUSSINESS_DB_URL', ''))
    result = pandas.read_sql_query(
    '''
        SELECT id, name, keywords FROM store_storeitem where store_id = %s and keywords IS NOT NULL
    ''' % store_id, bussiness_engine, index_col=['id'])

    d = collections.defaultdict(list)

    tags_query = pandas.read_sql_query(
    '''
        SELECT tag FROM standard_standardtag
    ''', bussiness_engine)
    tags = set(tags_query['tag'])
    for index, row in result.iterrows():
        for k in row.get('keywords'):
            tag_name = k.upper()
            if tag_name not in tags and len(tag_name) > 1:
                d[tag_name].append((index, row.get('name')))

    ordered_result = sorted(d.iteritems(),key=lambda (k,v): len(v),reverse=True)

    filtered_result = []
    for r in ordered_result:
        if len(r[1]) > 1:
            filtered_result.append(r)

    return filtered_result


def extract_brands(store_id):
    bussiness_engine = sqlalchemy.create_engine(environ.get('CM_BUSSINESS_DB_URL', ''))
    result = pandas.read_sql_query(
    '''
        SELECT id, name, keywords FROM store_storeitem where store_id = %s and keywords IS NOT NULL
    ''' % store_id, bussiness_engine, index_col=['id'])

    d = collections.defaultdict(list)

    brands_query = pandas.read_sql_query(
    '''
        SELECT tag FROM standard_standardtag WHERE type='brand'
    ''', bussiness_engine)
    brands = set(brands_query['tag'])

    # redis_client = redis.Redis(host = environ.get('CM_REDIS_URL', ''),
    #                            port = environ.get('CM_REDIS_PORT', ''),
    #                            password = environ.get('CM_REDIS_PASSWORD', ''),
    #                            db = environ.get('CM_REDIS_TAG_DB', ''))

    unbranded_items = []
    for index, row in result.iterrows():
        is_unbranded_item = True
        for k in row.get('keywords'):
            tag_name = k.upper()
            if tag_name in brands:
                d[tag_name].append((index, row.get('name'), row.get('keywords')))
                is_unbranded_item = False

        if is_unbranded_item:
            unbranded_items.append((index, row.get('name'), row.get('keywords')))

    ordered_result = sorted(d.iteritems(),key=lambda (k,v): len(v),reverse=True)

    return ordered_result, unbranded_items

def _get_score(item_tags, std_tags):
    item_tags_set = set(item_tags)
    std_tags_set = set(std_tags)
    print ', '.join(item_tags_set)
    print ', '.join(std_tags_set)
    score = len(item_tags_set & std_tags_set) / float(len(std_tags))
    print score
    print ''
    print ''

    return score

def match_items(store_id, brand_tag):
    bussiness_engine = sqlalchemy.create_engine(environ.get('CM_BUSSINESS_DB_URL', ''))
    store_items = pandas.read_sql_query(
    '''
        SELECT
            id,
            name,
            keywords,
            receipt_item_id,
            price
        FROM store_storeitem
        WHERE
            store_id = %s AND
            keywords IS NOT NULL AND
            keywords @> array['%s']
    ''' % (store_id, brand_tag), bussiness_engine, index_col=['id'])

    standard_items = pandas.read_sql_query(
    '''
    SELECT
        id,
        barcode,
        name,
        keywords,
        num_matches
    FROM
        standard_standarditem
    WHERE
        keywords @> array['%s'] AND
        num_matches > 0;
    '''  % brand_tag, bussiness_engine, index_col=['id'])

    d = collections.defaultdict()
    for i, ir in store_items.iterrows():
        d[ir.get('name')] = ''
        max_score = 0
        for j, jr in standard_items.iterrows():
            score = _get_score(ir.get('keywords'), jr.get('keywords'))
            if score > max_score:
                max_score = score
                d[ir.get('name')] = {'store_item': {'id': ir.get('id'),
                                                    'barcode': ir.get('receipt_item_id'),
                                                    'price': round(ir.get('price'), 1),
                                                    'keywords': ir.get('keywords')
                                                    },
                                     'standard_item': {'barcode': jr.get('barcode'),
                                                       'name': jr.get('name'),
                                                       'keywords': jr.get('keywords'),
                                                       'price': '0.0'
                                                       }
                                     }

    return d.items()