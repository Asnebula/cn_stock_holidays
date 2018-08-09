# cnhd (Chinese holiday especially for ticker trading)


[![Build Status](https://travis-ci.org/rainx/cn_stock_holidays.svg?branch=master)](https://travis-ci.org/rainx/cn_stock_holidays)

## 数据文件 (File Path)

沪深市场

```
cnhd/files/data_cn.txt
```

香港市场

```
cnhd/files/data_hk.txt
```


Fetch Data via URL :

```
wget https://raw.githubusercontent.com/Asnebula/cn_stock_holidays/master/cnhd/files/data_cn.txt

or

curl https://raw.githubusercontent.com/Asnebula/cn_stock_holidays/master/cnhd/files/data_hk.txt
```


## 文件内容 ( File Content)

保存除了周六日休市之外，其它休市信息，换行分割

store all (even upcoming) holiday for china stock exchange (without regular market close date on Saturday Day and Sun Day ) , one date per line

## 格式(File Format)
```
YYYYMMDD
```

## Python version

```
pip install git+https://github.com/asnebula/cn_stock_holidays.git
```

### 导入

```python

# 针对沪深
from cnhd import CalendarTool
ct=CalendarTool('CN')

# 针对香港
from cnhd import CalendarTool
ct=CalendarTool('HK')

```

FUNCTIONS

    Functions of instance of CalendarTool

    is_trading_day(dt)
        param dt: datetime.datetime or datetime.date.
        is a trading day or not
        :returns: Bool

    previous_trading_day(dt):
        param dt: datetime.datetime or datetime.date.
        get previous trading day
        :returns: datetime.date

    next_trading_day(dt):
        param dt: datetime.datetime or datetime.date.
        get next trading day
        :returns: datetime.date

    trading_days_between(start, end):

        param start, end: start and end time , datetime.datetime or datetime.date
        get calendar data range
        :returns: a generator for available dates for chinese market included start and end date
```

### about function cache

from version 0.10 on, we used functools.lrucache on `get_cached` for getting more speed,
if needed you can used the following syntax to clear cache.

```python
from cnhd import CalendarTool
ct=CalendarTool('CN')
ct.get_cached.cache_clear()

```


### Keep it up-to-date

we had a script to check the expired of the data and fetch the data from web.

you could set it up on cron job

```crontab
0 0 * * * path/to/cnhd-sync > /tmp/cnhd_sync.log
```

You could get the absolute path of cnhd-sync by which command

```bash
which cnhd-sync
```
