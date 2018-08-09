# -*- coding: utf-8 -*-
"""
Help functions for python to get china stock/future exchange holidays
"""
import logging
import os
import requests
from cnhd.common import *

CN_STOCK_FILE = 'data_cn.txt'
HK_STOCK_FILE = 'data_hk.txt'


class DataHelper:
    def __init__(self, exchange):
        if exchange == 'CN':
            self.data_file_name = CN_STOCK_FILE
        elif exchange == 'HK':
            self.data_file_name = HK_STOCK_FILE

    def get_local(self, use_list=False):
        """
        Read data from package data file(default is data_cn.txt in current directory)
        :return: a list contains all holiday data, element with datatime.date format
        """
        datafilepath = os.path.join(os.path.dirname(__file__), 'files', self.data_file_name)
        return get_from_file(datafilepath, use_list)

    def get_cache_path(self):
        """
        :return: '/home/YOURNAME/.cnhd/data_cn.txt' alike
        """
        usr_home = os.path.expanduser('~')
        cache_dir = os.path.join(usr_home, '.cnhd')
        if not (os.path.isdir(cache_dir)):
            os.mkdir(cache_dir)
        return os.path.join(cache_dir, self.data_file_name)

    # decoration from common.py, cache is bounded to instance so result is correct
    # TODO how to set 1 LRU cache to instances of 1 data_file_name is UNDONE
    @function_cache
    def get_cached(self, use_list=False):  # 由于在data.py里有function_cache装饰，该函数并不总是读文件，而是读缓存优先
        """
        get from cache version , if the cache file doesn't exist , use txt file in package data
        :return: a list/set contains all holiday data, element with datatime.date format
        """
        cache_path = self.get_cache_path()

        if os.path.isfile(cache_path):
            return get_from_file(cache_path, use_list)
        else:
            return self.get_local()

    def get_remote_and_cache(self):
        """
        get newest data file from network and cache on local machine
        :return: a list contains all holiday data, element with datatime.date format
        """
        response = requests.get(
            'https://raw.githubusercontent.com/Asnebula/cn_stock_holidays/master/cnhd/files/data_cn.txt')
        cache_path = self.get_cache_path()

        with open(cache_path, 'wb') as f:
            f.write(response.content)

        self.get_cached.cache_clear()  # 清除缓存（get_cached之前的调用结果），因为文件更新，需要读新的文件，而不能继续用之前的缓存

        return self.get_cached()  # 此时调用新文件已经存在，所以是新的结果

    def check_expired(self):
        """
        check if local or cached data need update
        :return: true/false
        """
        data = self.get_cached()
        now = datetime.datetime.now().date()
        for d in data:
            if d > now:
                return False
        return True

    def sync_data(self):
        logging.basicConfig(level=logging.INFO)
        if self.check_expired():
            logging.info("trying to fetch data...")
            self.get_remote_and_cache()
            logging.info("done")
        else:
            logging.info("local data is not expired, no need to fetch new data")


class CalendarTool(DataHelper):
    def is_trading_day(self, dt):
        if type(dt) is datetime.datetime:
            dt = dt.date()

        if dt.weekday() >= 5:
            return False
        holidays = self.get_cached()
        if dt in holidays:
            return False
        return True

    def previous_trading_day(self, dt):
        if type(dt) is datetime.datetime:
            dt = dt.date()

        while True:
            dt = dt - datetime.timedelta(days=1)
            if self.is_trading_day(dt):
                return dt

    def next_trading_day(self, dt):
        if type(dt) is datetime.datetime:
            dt = dt.date()

        while True:
            dt = dt + datetime.timedelta(days=1)
            if self.is_trading_day(dt):
                return dt

    def trading_days_between(self, start, end):
        if type(start) is datetime.datetime:
            start = start.date()

        if type(end) is datetime.datetime:
            end = end.date()

        dataset = self.get_cached()
        if start > end:
            return
        curdate = start
        while curdate <= end:
            if curdate.weekday() < 5 and not (curdate in dataset):
                yield curdate
            curdate = curdate + datetime.timedelta(days=1)


def main():
    d_cn = DataHelper('CN')
    d_hk = DataHelper('HK')
    d_cn.sync_data()
    d_hk.sync_data()
