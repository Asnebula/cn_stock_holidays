# -*- coding: utf-8 -*-
"""
Help functions for python to get china stock/future exchange holidays
"""
import logging
import os
import requests
from pandas.tslib import Timestamp as tp
from cnhd.common import *

CN_STOCK_FILE = 'data_cn.txt'
HK_STOCK_FILE = 'data_hk.txt'


class DataHelper:
    def __init__(self, exchange):
        if exchange == 'CN':
            self.data_file_name = CN_STOCK_FILE
        elif exchange == 'HK':
            self.data_file_name = HK_STOCK_FILE

    def get_local(self):
        """
        Read data from package data file(default is data_cn.txt in current directory)
        :return: a list contains all holiday data, element with datatime.date format
        """
        datafilepath = os.path.join(os.path.dirname(__file__), 'files', self.data_file_name)
        return get_from_file(datafilepath)

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
    def get_cached(self):  # 由于在data.py里有function_cache装饰，该函数并不总是读文件，而是读缓存优先
        """
        get from cache version , if the cache file doesn't exist , use txt file in package data
        :return: a list/set contains all holiday data, element with datatime.date format
        """
        cache_path = self.get_cache_path()

        if os.path.isfile(cache_path):
            return get_from_file(cache_path)
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
    @convert_arguments_to_datetime(['dt'])
    def is_trading_day(self, dt):
        dt = dt.date()
        if dt.weekday() >= 5:
            return False
        holidays = self.get_cached()
        if dt in holidays:
            return False
        return True

    @convert_arguments_to_datetime(['dt'])
    def previous_trading_day(self, dt, return_type=str):
        dt = dt.date()
        while True:
            dt = dt - datetime.timedelta(days=1)
            if self.is_trading_day(dt):
                if return_type == datetime.date:
                    return dt
                else:
                    d = datetime.datetime.combine(dt, datetime.datetime.min.time())
                    if return_type == datetime.datetime:
                        return d
                    elif return_type == str:
                        return d.strftime('%Y%m%d')
                    return d.strftime('%Y%m%d')

    @convert_arguments_to_datetime(['dt'])
    def next_trading_day(self, dt, return_type=str):
        dt = dt.date()
        while True:
            dt = dt + datetime.timedelta(days=1)
            if self.is_trading_day(dt):
                if return_type == datetime.date:
                    return dt
                else:
                    d = datetime.datetime.combine(dt, datetime.datetime.min.time())
                    if return_type == datetime.datetime:
                        return d
                    elif return_type == str:
                        return d.strftime('%Y%m%d')
                    return d.strftime('%Y%m%d')

    @convert_arguments_to_datetime(['start', 'end'])
    def trading_days_between(self, start, end, return_type=str):
        start = start.date()
        end = end.date()
        dataset = self.get_cached()
        if start > end:
            return
        curdate = start
        while curdate <= end:
            if curdate.weekday() < 5 and not (curdate in dataset):
                if return_type == datetime.date:
                    yield curdate
                else:
                    d = datetime.datetime.combine(curdate, datetime.datetime.min.time())
                    if return_type == datetime.datetime:
                        yield d
                    elif return_type == str:
                        yield d.strftime('%Y%m%d')
            curdate = curdate + datetime.timedelta(days=1)

    @convert_arguments_to_datetime(['dt'])
    def previous_n_trading_day(self, dt, n, return_type=str):
        # get workdays
        pre_day = self.previous_trading_day(dt, return_type=str)
        weekdays = get_periods_from_cad(end=pre_day, n=max(2 * n, 15))
        adhoc = set(tp(i) for i in self.get_cached())
        workdays = list(weekdays.difference(adhoc))
        workdays.sort()
        workdays = pd.DatetimeIndex(workdays)

        # get object date
        rs_datetime = workdays[workdays <= pd.to_datetime(pre_day)][-n].to_pydatetime()
        if return_type == datetime.datetime:
            return rs_datetime
        elif return_type == datetime.date:
            return rs_datetime.date()
        elif return_type == str:
            return rs_datetime.strftime('%Y%m%d')
        return rs_datetime.strftime('%Y%m%d')

    @convert_arguments_to_datetime(['dt'])
    def next_n_trading_day(self, dt, n, return_type=str):
        # get workdays
        next_day = self.next_trading_day(dt, return_type=str)
        weekdays = get_periods_from_cad(start=next_day, n=max(2 * n, 15))
        adhoc = set(tp(i) for i in self.get_cached())
        workdays = list(weekdays.difference(adhoc))
        workdays.sort()
        workdays = pd.DatetimeIndex(workdays)

        # get object date
        rs_datetime = workdays[workdays >= pd.to_datetime(next_day)][n - 1].to_pydatetime()
        if return_type == datetime.datetime:
            return rs_datetime
        elif return_type == datetime.date:
            return rs_datetime.date()
        elif return_type == str:
            return rs_datetime.strftime('%Y%m%d')
        return rs_datetime.strftime('%Y%m%d')


def main():
    d_cn = DataHelper('CN')
    d_hk = DataHelper('HK')
    d_cn.sync_data()
    d_hk.sync_data()
