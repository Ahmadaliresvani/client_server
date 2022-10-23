# importing the eel library  
import json
import datetime
import eel
import pandas as pd
import pytz
from tools.retrieve_data_meta import request_price
from tools import retrieve_data_meta
from tools.send_data import send_data_to_server
from tools.work_with_time import convert_time_interval_metatrader_time
import time

currency_request = ["btcusd"]
class JsonEncoderTimeStamp(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, obj)

# initializing the application  
eel.init("html_folder")

@eel.expose
def stop_btn_clicked():
    # clear history of retrive data
    retrieve_data_meta.last_time_downloaded = None


# get roboforex time 
def get_forex_time():
    tz = pytz.timezone("EET")
    return datetime.datetime.now(tz).replace(tzinfo=None)
        
# using the eel.expose command  
@eel.expose
# defining the function for addition of two numbers 
def get_data(user_id, url_address, time_interval):
    """this function used for get data from meta"""
    eel.insert_text("try for retrieve data from meta\n")
    
    result = request_price(
        currency_request, 
        convert_time_interval_metatrader_time(time_interval), 70, 5, eel.insert_text)

    if not result["state"]:
        eel.insert_text("we can't connect to metaTrader!!! please check connection..\n")
        eel.insert_text("sleep for 5 seconds and try agian....\n")
        time.sleep(5)
        get_data(user_id, url_address, time_interval)

    else:
        send_data(prepear_data(result["data"]), user_id=user_id, url_address=url_address)
        # define next time request
        # +03:00 time zone EET
        eel.start_stop_time_remaining("start", result["next_request_time"].strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"+03:00")

def prepear_data(data):
    if isinstance(data, dict):
        return json.dumps(data, cls=JsonEncoderTimeStamp)

    elif isinstance(data, pd.DataFrame):
        return data
    else:
        raise TypeError("only dict or dataframe sended to server!!!")


def send_data(data, user_id, url_address):
    """this function used for send data to server"""
    return_send = send_data_to_server(data=data, server_url=url_address, time_out=5, 
                header={"Content-Type":"application/json", "User-Id":user_id},methods="POST" , parameters=None)
    if return_send["state"]=='ok':
        eel.insert_text("successful send data to server\n")
        eel.insert_text(50*"-"+"\n")
    else:
        eel.insert_text(return_send["information"]+"\n")
        eel.insert_text("sleep for 5 seconds and try again\n")
        time.sleep(5)
        eel.insert_text("start another connect to server....\n")
        send_data(data, user_id, url_address)


      
# starting the application  
eel.start("main.html")
