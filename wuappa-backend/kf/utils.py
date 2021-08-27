# -*- coding: utf-8 -*-
import csv
import os
from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework.pagination import PageNumberPagination


class GenericUtils(object):
    @staticmethod
    def xround(a, b):
        c = pow(10, b)
        return round(a * c) / c

    @staticmethod
    def dictfetchall(cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    @staticmethod
    def check_dir_or_create(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def my_import(klass):
        parser_path = klass.rsplit('.', 1)[0]
        parser_name = klass.rsplit('.', 1)[1]
        mod = __import__(parser_path)
        components = parser_path.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)

        mod = getattr(mod, parser_name)
        return mod

    @staticmethod
    def adjust_date_to_next_day_to_filter(date):
        if date is not None and date != '':
            return datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
        else:
            return ''

    @staticmethod
    def merge_dicts(*dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    @staticmethod
    def convert_account_to_iban_if_needed(account):
        if account[:2].upper() == "ES":
            return account.upper()
        try:
            ccc = int(account + "142800")
            iban = 98 - (ccc % 97)
        except ValueError:
            return ''
        return "ES{:0>2d}".format(iban) + account


class GenericFilter(object):
    @classmethod
    def filter(cls, request, ordering_list, search_list, filters_list):
        args, kwargs, ordering = cls.generic_filters_params(request, ordering_list, search_list, filters_list)
        return args, kwargs, ordering

    @staticmethod
    def generic_filters_params(get_attr, ordering_list, search_list, filters_list):

        kwargs = {}
        for attr in get_attr:
            # Check if element is in filter list
            if attr in filters_list and get_attr[attr] != '':
                kwargs[attr] = fix_bool(get_attr[attr])

            else:
                if any(attr in d for d in filters_list) and get_attr[attr] != '':
                    for el in filters_list:
                        if attr in el:
                            kwargs[el[attr]] = fix_bool(get_attr[attr])
                            break

        args = Q()
        filter_elements = []
        if 'q' in get_attr and get_attr['q'] != '':
            query = get_attr['q']
            for element in search_list:
                filter_elements.append((element + '__icontains', query))

            args.children = filter_elements
            args.connector = args.OR

        if 'ids' in get_attr and get_attr['ids'] != '':
            kwargs['id__in'] = get_attr['ids'].split(',')

        # Check ordering
        ordering = ''
        if 'ordering' in get_attr and get_attr['ordering'] != '':
            order_param = get_attr['ordering']
            if order_param[:1] == '-':
                order_param = order_param[1:]
            if order_param in ordering_list:
                ordering = get_attr['ordering']

        return args, kwargs, ordering


def fix_bool(value):
    if isinstance(value, str):
        if value.lower() == 'false':
            return False
        if value.lower() == 'true':
            return True
    return value


def is_csv_file(filename, delimiter):
    errors = []
    try:
        csv_fileh = open(filename, 'rb')
        # Perform various checks on the dialect (e.g., lineseparator, delimiter) to make sure it's sane
        csv.Sniffer().sniff(csv_fileh.read(), delimiter)
        # Don't forget to reset the read position back to the start of the file before reading any entries.
        csv_fileh.seek(0)
        csv_fileh.close()
    except csv.Error as e:
        errors.append(e)
    except (IOError, OSError) as e:
        errors.append(e)
    return errors


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


# For json.dumps (datetime not serializable)
def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError
