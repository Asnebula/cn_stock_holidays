# -*- coding: utf-8 -*-

import datetime
'''
一些类型转换函数和其他
'''


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


def get_from_file(filename, use_list=False):
    with open(filename, 'r') as f:
        data = f.readlines()
        if use_list:
            return [int_to_date(str_to_int(i.rstrip('\n'))) for i in data]
        else:
            return set([int_to_date(str_to_int(i.rstrip('\n'))) for i in data])
