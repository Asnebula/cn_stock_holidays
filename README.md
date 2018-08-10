# cnhd (Chinese holiday especially for ticker trading)


[![Build Status](https://travis-ci.org/Asnebula/cn_stock_holidays.svg?branch=master)](https://travis-ci.org/Asnebula/cn_stock_holidays)

## 数据文件 (File Path)
沪深市场
```
cnhd/files/data_cn.txt
```
香港市场
```
cnhd/files/data_hk.txt
```
通过URL获取 (Fetch Data via URL) :
```
wget https://raw.githubusercontent.com/Asnebula/cn_stock_holidays/master/cnhd/files/data_cn.txt
or
curl https://raw.githubusercontent.com/Asnebula/cn_stock_holidays/master/cnhd/files/data_hk.txt
```
文件内容 ( File Content)
```
保存除了周六日休市之外，其它休市信息，换行分割
store all (even upcoming) holiday for china stock exchange (without regular market close date on Saturday Day and Sun Day ) ,
one date per line.
```
格式(File Format)
```
YYYYMMDD
```

## pip安装 (install through pip)
```
pip install git+https://github.com/asnebula/cn_stock_holidays.git
```

## 导入 (imports)
```python

# 针对沪深
from cnhd import CalendarTool
ct = CalendarTool('CN')

# 针对香港
from cnhd import CalendarTool
ct = CalendarTool('HK')

# zipline支持部分（前提：zipline已经安装）
from cnhd.zpl import reg_cal
reg_cal('HKEX')  # SHSZ if 沪深市场
hk_cad = get_calendar('HKEX')  # SHSZ if 沪深市场
```

## API函数（CalendarTool实例可用） (Functions of instance of CalendarTool)
```
    is_trading_day(dt)
        param dt: str,datetime.datetime or datetime.date.
        is a trading day or not
        :returns: Bool

    previous_trading_day(dt,return_type=str):
        param dt: str,datetime.datetime or datetime.date.
        get previous trading day
        :returns: str,datetime.datetime or datetime.date according to value of return_type

    next_trading_day(dt,return_type=str):
        param dt: str,datetime.datetime or datetime.date.
        get next trading day
        :returns: str,datetime.datetime or datetime.date according to value of return_type
    
    previous_n_trading_day(dt,n,return_type=str):
        param dt: str,datetime.datetime or datetime.date.
        param n: int, number of previous trading days 
        get the previous n trading day
        :returns: str,datetime.datetime or datetime.date according to value of return_type
    
    next_n_trading_day(dt,n,return_type=str):
        param dt: str,datetime.datetime or datetime.date.
        param n: int, number of next trading days 
        get the next n trading day
        :returns: str,datetime.datetime or datetime.date according to value of return_type

    trading_days_between(start, end,return_type=str):
        param start, end: start and end time , datetime.datetime or datetime.date
        get calendar data range
        :returns: a generator for available dates for chinese market included start and end date
```

## Bash命令 ( Bash command)
we can get trading days of a date range in bash using `get-day-list` command , output format YYYY-MM-DD
```
get-day-list -m HK -s 20180101 -e 20180301
```

## 保持数据最新 (Keep it up-to-date)
we had a script to check the expired of the data and fetch the data from web.
you could set it up on cron job

```crontab
0 0 * * * path/to/cnhd-sync > /tmp/cnhd_sync.log
```

You could get the absolute path of cnhd-sync by `which` command

```bash
which cnhd-sync
```

## 其他 (miscellaneous)
### 有关缓存 (about function cache)
from version 0.10 on, we used functools.lrucache on `get_cached` for getting more speed,
if needed you can used the following syntax to clear cache.

```python
from cnhd import CalendarTool
ct = CalendarTool('CN')
ct.get_cached.cache_clear()

```
