# -*- coding: utf-8 -*-

from zipline.utils.calendars import (
    clear_calendars,
    deregister_calendar,
    get_calendar,
    register_calendar,
    register_calendar_alias,
    register_calendar_type,
    TradingCalendar,
)
from .exchange_calendar_shsz import SHSZExchangeCalendar
from .exchange_calendar_hkex import HKExchangeCalendar

_additional_calendar_factories = {
    'SHSZ': SHSZExchangeCalendar,
    'HKEX': HKExchangeCalendar,
}
_additional_calendar_aliases = {
    'ShangHaiA': 'SHSZ',
    'ShenZhenA': 'SHSZ',
    'HongKongH': 'HKEX',
}


def reg_cal(real_name, force=True):
    register_calendar(real_name, _additional_calendar_factories[real_name], force=force)

    def _f(a):
        for k, v in a.items():
            if k == real_name:
                return k
            else:
                return ''

    register_calendar_alias(_f(_additional_calendar_aliases), real_name, force=force)
    register_calendar_type(real_name, _additional_calendar_factories[real_name], force=force)
