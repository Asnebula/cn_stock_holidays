# -*- coding: utf-8 -*-
"""
Help functions for python to get china stock exchange holidays
"""
from cn_stock_holidays.meta_functions import *

DATA_FILE_FOR_SHSZ = "data.txt"

get_local = meta_get_local(data_file_name=DATA_FILE_FOR_SHSZ)
get_cache_path = meta_get_cache_path(data_file_name=DATA_FILE_FOR_SHSZ)


# decoration from common.py
@function_cache
def get_cached(use_list=False):
    return meta_get_cached(get_local=get_local, get_cache_path=get_cache_path)(use_list=use_list)


get_remote_and_cache = meta_get_remote_and_cache(get_cached=get_cached, get_cache_path=get_cache_path)

check_expired = meta_check_expired(get_cached=get_cached)
sync_data = meta_sync_data(check_expired=check_expired, get_remote_and_cache=get_remote_and_cache)

is_trading_day = meta_is_trading_day(get_cached=get_cached)
previous_trading_day = meta_previous_trading_day(is_trading_day=is_trading_day)
next_trading_day = meta_next_trading_day(is_trading_day=is_trading_day)
trading_days_between = meta_trading_days_between(get_cached=get_cached)
