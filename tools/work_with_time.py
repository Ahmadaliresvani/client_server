import datetime
from time import time
import pytz
import MetaTrader5 as mt

def get_forex_time():
    return datetime.datetime.now(pytz.timezone("EET"))

def get_forex_time_naive():
    return datetime.datetime.now(pytz.timezone("EET")).replace(tzinfo=None)

def convert_time_interval_metatrader_time(time_name):
    if time_name == '1m':
        return mt.TIMEFRAME_M1
    elif time_name == '5m':
        return mt.TIMEFRAME_M5
    elif time_name == '10m':
        return mt.TIMEFRAME_M10
    elif time_name == '15m':
        return mt.TIMEFRAME_M15
    elif time_name == '30m':
        return mt.TIMEFRAME_M30
    elif time_name == '1h':
        return mt.TIMEFRAME_H1
    elif time_name == '4h':
        return mt.TIMEFRAME_H4
    else:
        raise ValueError("time interval not allowed")
