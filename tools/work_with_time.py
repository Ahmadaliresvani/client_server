import datetime
import MetaTrader5 as Mt
import os
import pytz

dir_path = os.path.dirname(os.path.abspath(__file__))


def get_forex_time():
    return datetime.datetime.now(pytz.timezone("EET"))


def get_forex_time_naive():
    return datetime.datetime.now(pytz.timezone("EET")).replace(tzinfo=None)


def convert_time_interval_metatrader_time(time_name):
    if time_name == '1m':
        return Mt.TIMEFRAME_M1
    elif time_name == '5m':
        return Mt.TIMEFRAME_M5
    elif time_name == '10m':
        return Mt.TIMEFRAME_M10
    elif time_name == '15m':
        return Mt.TIMEFRAME_M15
    elif time_name == '30m':
        return Mt.TIMEFRAME_M30
    elif time_name == '1h':
        return Mt.TIMEFRAME_H1
    elif time_name == '4h':
        return Mt.TIMEFRAME_H4
    else:
        raise ValueError("time interval not allowed")


def convert_metatrader_time_to_delta_time(meta_time):
    if meta_time == Mt.TIMEFRAME_M1:
        return datetime.timedelta(minutes=1)
    elif meta_time == Mt.TIMEFRAME_M5:
        return datetime.timedelta(minutes=5)
    elif meta_time == Mt.TIMEFRAME_M10:
        return datetime.timedelta(minutes=10)
    elif meta_time == Mt.TIMEFRAME_M15:
        return datetime.timedelta(minutes=15)
    elif meta_time == Mt.TIMEFRAME_M30:
        return datetime.timedelta(minutes=30)
    elif meta_time == Mt.TIMEFRAME_H1:
        return datetime.timedelta(hours=1)
    elif meta_time == Mt.TIMEFRAME_H4:
        return datetime.timedelta(hours=4)
    else:
        raise ValueError("meta time interval not allowed")
