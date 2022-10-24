import datetime
import json
import os
import csv
import time
import eel
import pandas as pd
import pytz
from root_dir import root_dir
from tools import retrieve_data_meta
from tools.logger_code import create_logger
from tools.retrieve_data_meta import request_price
from tools.send_data import send_data_to_server
from tools.work_with_time import convert_time_interval_metatrader_time

# create report dir (for save logger) if need(not exists)!!
if not os.path.exists(os.path.join(root_dir, "report_dir")):
    os.mkdir(os.path.join(root_dir, "report_dir"))

currency_request = ["eurusd", "audjpy"]

# create logger for main
main_logger = create_logger("main_logger", os.path.join(root_dir, "report_dir"))
main_logger.info("start program")


class JsonEncoderTimeStamp(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, obj)


# initializing the application
eel.init("html_folder")


@eel.expose
def stop_btn_clicked():
    # clear history of retrieve data
    retrieve_data_meta.last_time_downloaded = None
    main_logger.log("stop btn clicked")


# get robo-forex time
def get_forex_time():
    tz = pytz.timezone("EET")
    return datetime.datetime.now(tz).replace(tzinfo=None)


# using the eel.expose command  
@eel.expose
# defining the function for addition of two numbers 
def get_data(user_id, url_address, time_interval):
    """this function used for get data from meta"""
    eel.insert_text("try for retrieve data from meta\n")
    main_logger.info("request from js to get data")
    result = request_price(
        currency_request,
        convert_time_interval_metatrader_time(time_interval), 70, 5, eel.insert_text)

    if not result["state"]:
        main_logger.info("unsuccessful in request price from meta")
        eel.insert_text("we can't connect to metaTrader!!! please check connection..\n")
        eel.insert_text("sleep for 5 seconds and try agian....\n")
        time.sleep(5)
        get_data(user_id, url_address, time_interval)

    else:
        main_logger.info("successful in request price from meta")
        main_logger.info("start send data to server")
        send_data(prepare_data(result["data"]), user_id=user_id, url_address=url_address)
        # define next time request
        # +03:00 time zone EET
        eel.start_stop_time_remaining("start",
                                      result["next_request_time"].strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+03:00")


def prepare_data(data):
    main_logger.info("start prepare data for send to server")
    if isinstance(data, dict):
        main_logger.info("data type is dict and convert to json")
        return json.dumps(data, cls=JsonEncoderTimeStamp)

    elif isinstance(data, pd.DataFrame):
        main_logger.info("data type is dataframe and not need convert")
        return data
    else:
        main_logger.info("error in data type, data tye=={}".format(type(data)))
        raise TypeError("only dict or dataframe sent to server!!!")


def send_data(data, user_id, url_address):
    """this function used for send data to server"""
    return_send = send_data_to_server(data=data, server_url=url_address, time_out=5,
                                      header={"Content-Type": "application/json", "User-Id": user_id}, methods="POST",
                                      parameters=None)
    main_logger.info("return state from server== {}".format(return_send))
    if return_send["state"] == 'ok':

        main_logger.info("successful send data to server...")
        eel.insert_text("successful send data to server\n")
        eel.insert_text(50 * "-" + "\n")
    else:
        main_logger.info("unsuccessful send data to server sleep for 5 seconds and try again")
        eel.insert_text(return_send["information"] + "\n")
        eel.insert_text("sleep for 5 seconds and try again\n")
        time.sleep(5)
        eel.insert_text("start another connect to server....\n")
        send_data(data, user_id, url_address)


# starting the application
eel.start("main.html")
