from __future__ import annotations
from datetime import datetime
import pytz
import requests, os
import pandas as pd
from root_dir import root_dir
from tools.logger_code import create_logger

send_data_logger = create_logger("send_data_to_server", dir_name=os.path.join(root_dir, "report_dir"))


def send_data_to_server(data: dict | pd.DataFrame, server_url: str, time_out: float,
                        header: dict, methods: str = 'POST', parameters=None):
    """This function used for send data to specific server
    Parameters: 
        methods:
        data: a json file that send to server (out put like: {"columns":[....], "data":[.....]})
        server_url: a server address (or any url that we must send data to it) in string
        time_out: a time-out for send request to server (after finish timeout return error code)
        header: a data than pass as header in request to server
        parameters : if methods(requests type) is GET, we use parameters as dict (key:value) for query string
    """
    send_data_logger.info("start send to server")
    # cheak data type and contents...
    if isinstance(data, pd.DataFrame):
        send_data_logger.info("data type is data Frame and convert to json")
        data = data.to_json(orient='split', index=False)
    elif isinstance(data, dict):
        send_data_logger.info("data type is dict and convert to string")
        data = str(data)
    # check methods content
    if methods.upper() in ['POST', 'GET']:
        send_data_logger.info("type of request is get or post")
        pass
    else:
        send_data_logger.info("methods for send is illegal (only get or post)")
        raise ValueError("methods must be get or post")

    if methods.upper() == 'POST':
        send_data_logger.info("methods is post and add Send-Time, url, data, timeout")
        header["Send-Time"] = datetime.now(pytz.timezone("EET")).strftime("%H:%M:%S")
        fields = {"url": server_url, "data": data, "headers": header, "timeout": time_out}
        request_fun = requests.post
    elif methods.upper() == 'GET':
        send_data_logger.info("methods is get and url, parameter: {}, timeout".format(parameters))
        fields = {"url": server_url, "params": parameters, "timeout": time_out}
        request_fun = requests.get
    try:
        send_data_logger.info("try for request")
        return_result = request_fun(**fields)
        if return_result.status_code == 200:
            send_data_logger.info("status code is 200 and everything is oK")
            return_result = {"state": 'ok'}
        else:
            send_data_logger.info("status code is not 200 and a problem occurred!!!")
    except requests.exceptions.ConnectTimeout:
        send_data_logger.info("connection time out error")
        return_result = {'state': 'error', 'information': 'connection time out'}
    except requests.exceptions.InvalidHeader:
        send_data_logger.info("Invalid header error")
        return_result = {'state': 'error', 'information': 'header error'}
    except requests.exceptions.ConnectionError:
        send_data_logger.info("connection error")
        return_result = {'state': 'error', 'information': 'connection error'}

    return return_result
