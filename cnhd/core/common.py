# -*- coding: utf-8 -*-

import datetime
from functools import wraps
from dateutil import parser
from pandas.tseries.offsets import CustomBusinessDay
import pandas as pd
import sys

'''
一些类型转换函数和其他
'''
if sys.version_info.major == 2:
    def function_cache(f):
        memo = {}

        @wraps(f)
        def wrapper(*args, **kwargs):
            if args in memo:
                return memo[args]
            else:
                rv = f(*args, **kwargs)
                memo[args] = rv
                return rv

        def cache_clear():
            global memo
            memo = {}

        wrapper.cache_clear = cache_clear
        return wrapper
else:  # suppose it is 3 or larger
    from functools import lru_cache

    function_cache = lru_cache(None, typed=True)  # 缓存函数调用结果


def int_to_date(d):
    d = str(d)
    return datetime.date(int(d[:4]), int(d[4:6]), int(d[6:]))


def date_to_str(da):
    return da.strftime("%Y%m%d")


def str_to_int(s):
    return int(s)


def date_to_int(da):
    return str_to_int(date_to_str(da))


def print_result(s):
    print("-" * 20)
    print("*" + str(s) + "*")
    print("-" * 20)
    print("")


def get_from_file(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
        return [int_to_date(str_to_int(i.rstrip('\n'))) for i in data]


def convert_arguments_to_datetime(arguments):
    def make_wrapper(func):
        def wrapper(*args, **kwargs):
            # 拿到被装饰函数的参数名列表
            code = func.__code__
            names = list(code.co_varnames[:code.co_argcount])
            # args类型是tuple, tuple是不可变对象
            args_in_list = list(args)
            # 装饰arguments
            for argument in arguments:
                num = names.index(argument)
                value = args[num]
                if isinstance(value, str):
                    value = parser.parse(value)
                elif isinstance(value, datetime.date):
                    value = datetime.datetime.combine(value, datetime.datetime.min.time())
                args_in_list[num] = value
            new_args = tuple(args_in_list)
            return func(*new_args, **kwargs)

        return wrapper

    return make_wrapper


def get_periods_from_cad(start=None, end=None, n=None):
    weekmask = 'Mon Tue Wed Thu Fri'
    cbd = CustomBusinessDay(weekmask=weekmask)
    weekdays = pd.date_range(start=start, end=end, periods=n, freq=cbd)
    return set(weekdays)
