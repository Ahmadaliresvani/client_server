import MetaTrader5 as mt
import pandas as pd
import time
from tools.work_with_time import get_forex_time_naive

last_time_downloaded = None


def request_price(currency_name, time_interval:int, number_retrieve_rows:int,
                    sleep_time_for_wait:float, object_for_report):
    global last_time_downloaded

    return_data = {'state':False}
    if not mt.initialize(timeout=10000):
        return return_data
    data = {}
    for name in currency_name:
        object_for_report(f"start download data for {name.upper()}.\n")

        while True:
            rates = mt.copy_rates_from_pos(name.upper(), time_interval, 0, number_retrieve_rows)

            rates_frame = pd.DataFrame(rates)
            rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
            pre_last_frame_time = rates_frame.iloc[-2]["time"]
            last_frame_time = rates_frame.iloc[-1]["time"]
            if last_frame_time < get_forex_time_naive():
                if last_frame_time != last_time_downloaded:
                    # we change last time request when finish all request
                    object_for_report(f"data for {name.upper()} downloaded.\n")
                    data[name] = rates_frame.to_dict(orient='list')
                    next_time_request = last_frame_time + (last_frame_time-pre_last_frame_time)
                    break
                else:
                    object_for_report(f"candle time lower system time but , not created new candle.\n")
                    object_for_report("system time: {}, datatime: {}, last downloaded time: {}.\n".format(
                        get_forex_time_naive().strftime("%H:%M:%S"),
                        last_frame_time.strftime("%H:%M:%S"),
                        last_time_downloaded.strftime("%H:%M:%S")
                    ))
                    time.sleep(1)
                    continue
            else:
                # we need new data....
                object_for_report("data time lower system time!!ststem time: {}, datatime: {}.".format(
                    get_forex_time_naive().strftime("%H:%M:%S"),
                    last_frame_time.strftime("%H:%M:%S")
                ))
                time.sleep(1)
                continue


    return_data['state']=True
    return_data['data']=data
    return_data["next_request_time"]=next_time_request
    last_time_downloaded  = last_frame_time
    return return_data

