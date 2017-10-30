# -*- coding: utf-8 -*-
"""
This model defineds the base class for custom model.
A custom model is the model that doesn't map with django's ORM system
Thus it works we existing table and won't be affected by django's
model migration
"""

from django.utils import six
from django.db import connection
import pandas
import copy
import logging
logger = logging.getLogger(__name__)


class CustomModelOption(object):

    def __init__(self, options=None):
        # TODO: verity table_name must be defined
        self.table = getattr(options, 'table_name', None)


class CustomModelMeta(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(CustomModelMeta, cls).__new__(
            cls, name, bases, attrs)
        parents = [b for b in bases if isinstance(b, CustomModelMeta)]

        if not parents:
            return new_class

        new_class._meta = CustomModelOption(
            getattr(new_class, 'Meta', None))

        return new_class


class CustomModel(six.with_metaclass(CustomModelMeta)):
    @staticmethod
    def gen_select_clause(table_name, column_names, params):
        holders = ','.join(column_names)
        query = 'SELECT %s FROM %s' % (holders, table_name)
        return query

    @staticmethod
    def gen_where_clause(filters, params):
        # TODO: verify the fields are valid from the table schema.
        where_s = []
        where_template = '%s = %%s'
        for key, item in six.iteritems(filters):
            print(type(item))
            if type(item) is list:
                in_template = ','.join(['%s' for _ in item])
                where_s.append('{key} IN ({vals})'.format(
                    key=key, vals=in_template))
                params.extend(item)
            else:
                where_s.append(where_template % key)
                # TODO: handle greater / smaller (__lt, __gt, etc.)
                params.append(item)

        if where_s:
            return '\nWHERE\n  ' + '\nAND\n  '.join(where_s)
        else:
            return ''

    @staticmethod
    def gen_count_query(table_name, filters=None):
        filters.pop('s', None)
        filters.pop('o', None)
        filters.pop('offset', None)
        filters.pop('limit', None)
        if table_name is None:
            raise ValueError('table_name cannot be none')

        if filters is None:
            return ('SELECT COUNT(*) FROM %s' % table_name, [])

        query = 'SELECT COUNT(*) FROM %s' % table_name
        params = []
        query = query + CustomModel.gen_where_clause(filters, params)
        return (query, params)

    @staticmethod
    def gen_query(table_name, filters=None):
        if table_name is None:
            raise ValueError('table_name cannot be none')

        if filters is None:
            return ('SELECT * FROM %s' % table_name, [])

        params = []
        columns = filters.pop('s', ['*'])
        query = CustomModel.gen_select_clause(table_name, columns, params)
        # note that we only support order by sinlge field at this moment
        order = filters.pop('o', None)
        limit = filters.pop('limit', None)
        offset = filters.pop('offset', None)
        query = query + CustomModel.gen_where_clause(filters, params)

        if order:
            # TODO: handle ascending and descending
            query = query + '\nORDER BY %s DESC' % order

        if limit:
            query = query + '\nLIMIT %s'
            params.append(str(limit))

        if offset:
            query = query + '\nOFFSET %s'
            params.append(str(offset))

        return (query, params)

    @classmethod
    def get_objects(cls, filters):
        filters = copy.deepcopy(filters)
        query = cls.gen_query(cls._meta.table, filters)
        logger.info('Query: \n' + str(query[0]))
        logger.info('Parameters:' + str(query[1]))
        data = pandas.read_sql_query(sql=query[0],
                                     params=query[1],
                                     con=connection)
        return [row.to_dict() for _, row in data.iterrows()]

    @classmethod
    def get_count(cls, filters):
        filters = copy.deepcopy(filters)
        query = cls.gen_count_query(cls._meta.table, filters)
        with connection.cursor() as cursor:
            cursor.execute(query[0], query[1])
            return cursor.fetchone()[0]
