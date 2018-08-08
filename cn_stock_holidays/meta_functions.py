# -*- coding: utf-8 -*-

import datetime
import logging
import os
import requests
from cn_stock_holidays.common import _get_from_file


# meta func is not a good design, but for backward compatibility for data version and create similar logic for hk,
# we did it

def meta_get_local(data_file_name='data.txt'):
    def get_local(use_list=False):
        """
        Read data from package data file(default is data.txt in current directory)
        :return: a list contains all holiday data, element with datatime.date format
        """
        datafilepath = os.path.join(os.path.dirname(__file__), data_file_name)
        return _get_from_file(datafilepath, use_list)

    return get_local


def meta_get_cache_path(data_file_name='data.txt'):
    def get_cache_path():
        """
        :return: '/home/YOURNAME/.cn_stock_holidays/data.txt' alike
        """
        usr_home = os.path.expanduser('~')
        cache_dir = os.path.join(usr_home, '.cn_stock_holidays')
        if not (os.path.isdir(cache_dir)):
            os.mkdir(cache_dir)
        return os.path.join(cache_dir, data_file_name)

    return get_cache_path


def meta_get_cached(get_local, get_cache_path):
    def get_cached(use_list=False):  # 由于在data.py里有function_cache装饰，该函数并不总是读文件，而是读缓存优先
        """
        get from cache version , if the cache file doesn't exist , use txt file in package data
        :return: a list/set contains all holiday data, element with datatime.date format
        """
        cache_path = get_cache_path()

        if os.path.isfile(cache_path):
            return _get_from_file(cache_path, use_list)
        else:
            return get_local(use_list=False)

    return get_cached


def meta_get_remote_and_cache(get_cached, get_cache_path):
    def get_remote_and_cache():
        """
        get newest data file from network and cache on local machine
        :return: a list contains all holiday data, element with datatime.date format
        """
        response = requests.get(
            'https://raw.githubusercontent.com/Asnebula/cn_stock_holidays/master/cn_stock_holidays/data.txt')
        cache_path = get_cache_path()

        with open(cache_path, 'wb') as f:
            f.write(response.content)

        get_cached.cache_clear()  # 清除缓存（get_cached之前的调用结果），因为文件更新，需要读新的文件，而不能继续用之前的缓存

        return get_cached()  # 此时调用新文件已经存在，所以是新的结果

    return get_remote_and_cache


def meta_check_expired(get_cached):
    def check_expired():
        """
        check if local or cached data need update
        :return: true/false
        """
        data = get_cached()
        now = datetime.datetime.now().date()
        for d in data:
            if d > now:
                return False
        return True

    return check_expired


def meta_sync_data(check_expired, get_remote_and_cache):
    def sync_data():
        logging.basicConfig(level=logging.INFO)
        if check_expired():
            logging.info("trying to fetch data...")
            get_remote_and_cache()
            logging.info("done")
        else:
            logging.info("local data is not expired, no need to fetch new data")

    return sync_data


def meta_is_trading_day(get_cached):
    def is_trading_day(dt):
        if type(dt) is datetime.datetime:
            dt = dt.date()

        if dt.weekday() >= 5:
            return False
        holidays = get_cached()
        if dt in holidays:
            return False
        return True

    return is_trading_day


def meta_previous_trading_day(is_trading_day):
    def previous_trading_day(dt):
        if type(dt) is datetime.datetime:
            dt = dt.date()

        while True:
            dt = dt - datetime.timedelta(days=1)
            if is_trading_day(dt):
                return dt

    return previous_trading_day


def meta_next_trading_day(is_trading_day):
    def next_trading_day(dt):
        if type(dt) is datetime.datetime:
            dt = dt.date()

        while True:
            dt = dt + datetime.timedelta(days=1)
            if is_trading_day(dt):
                return dt

    return next_trading_day


def meta_trading_days_between(get_cached):
    def trading_days_between(start, end):
        if type(start) is datetime.datetime:
            start = start.date()

        if type(end) is datetime.datetime:
            end = end.date()

        dataset = get_cached()
        if start > end:
            return
        curdate = start
        while curdate <= end:
            if curdate.weekday() < 5 and not (curdate in dataset):
                yield curdate
            curdate = curdate + datetime.timedelta(days=1)

    return trading_days_between
