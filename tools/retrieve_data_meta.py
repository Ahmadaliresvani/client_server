import MetaTrader5 as Mt
import pandas as pd
import time, os
from tools.logger_code import create_logger
from tools.work_with_time import get_forex_time_naive, convert_metatrader_time_to_delta_time
from root_dir import root_dir

retrieve_logger = create_logger("retrieve_looger", os.path.join(root_dir, "report_dir"))

last_time_downloaded = None


def request_price(currency_name, time_interval: int, number_retrieve_rows: int,
                  sleep_time_for_wait: float, object_for_report):
    global last_time_downloaded
    retrieve_logger.info("start retrieve data from meta")
    return_data = {'state': False}
    if not Mt.initialize(timeout=10000):
        retrieve_logger.info("after 10 seconds not initial metaTrader")
        return return_data
    retrieve_logger.info("successful initial metaTrader")

    data = {}
    for name in currency_name:
        object_for_report("start download data for {}.\n".format(name.upper()))
        retrieve_logger.info("start download data from meta for {}".format(name))
        while True:
            rates = Mt.copy_rates_from_pos(name.upper(), time_interval, 0, number_retrieve_rows)

            rates_frame = pd.DataFrame(rates)
            rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
            pre_last_frame_time = rates_frame.iloc[-2]["time"]
            last_frame_time = rates_frame.iloc[-1]["time"]
            # if abs space greater than time interval try again
            if abs(last_frame_time - get_forex_time_naive()) > convert_metatrader_time_to_delta_time(time_interval):
                retrieve_logger.info(
                    "space between request time and data time greater than time interval after 2 seconds try again")
                retrieve_logger.info("last frame time: {}, system time: {}, interval: {}".format(
                    last_frame_time, get_forex_time_naive(), convert_metatrader_time_to_delta_time(time_interval)
                ))
                object_for_report(
                    "space between now time and meta time greater than interval ...after 2 seconds try again\n")
                time.sleep(2)
                continue
            if last_frame_time < get_forex_time_naive():
                retrieve_logger.info("last time frame < system time : {} < {}".format(
                    last_frame_time, get_forex_time_naive()))
                if last_frame_time != last_time_downloaded:
                    retrieve_logger.info("last time frame != last time downloaded , {}!={}".format(
                        last_frame_time, last_time_downloaded
                    ))
                    # we change last time request when finish all request
                    object_for_report(f"data for {name.upper()} downloaded.\n")
                    data[name] = rates_frame.to_dict(orient='list')
                    next_time_request = last_frame_time + (last_frame_time - pre_last_frame_time)
                    break
                else:
                    retrieve_logger.info(
                        "last frame time == last time downloaded, {}=={}, sleep for 1 seconds and try again".format(
                            last_frame_time, last_time_downloaded
                        ))
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
                retrieve_logger.info("last time frame >= system time : {} >= {}".format(
                    last_frame_time, get_forex_time_naive()
                ))
                retrieve_logger.info("sleep for 1 seconds and try again")
                object_for_report("data time lower system time!!ststem time: {}, datatime: {}.".format(
                    get_forex_time_naive().strftime("%H:%M:%S"),
                    last_frame_time.strftime("%H:%M:%S")
                ))
                time.sleep(1)
                continue

    return_data['state'] = True
    return_data['data'] = data
    return_data["next_request_time"] = next_time_request
    last_time_downloaded = last_frame_time
    return return_data
