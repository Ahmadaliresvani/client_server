from __future__ import annotations
from datetime import datetime
import pytz
import requests
import pandas as pd

def send_data_to_server(data:dict|pd.DataFrame, server_url:str, time_out:float, 
                header:dict,methods:str='POST' , parameters=None):
    """This function used for send data to specifiec server
    Parameters: 
        data: a json file that send to server (out put like: {"columns":[....], "data":[.....]})
        server_url: a server adreess (or any url that we must send data to it) in string
        time_out: a time out for send request to server (after finish timeout return eerror code)
        header: a data than pass as header in request to server
        parameters : if methods(requests type) is GET, we use parameters as dict (key:value) for query string
    """
    
    # cheak data type and contents...
    if isinstance(data, pd.DataFrame):
        data = data.to_json(orient='split', index=False)
    elif isinstance(data, dict):
        data = str(data)
    # check methods content
    if methods.upper() in ['POST', 'GET']:
        pass
    else:
        raise ValueError("methods must be get or post")
    
    if methods.upper() == 'POST':
        header["Send-Time"] = datetime.now(pytz.timezone("EET")).strftime("%H:%M:%S")
        fields = {"url":server_url,"data":data, "headers":header, "timeout":time_out}
        request_fun = requests.post   
    elif methods.upper() == 'GET':
        fields = {"url":server_url,"params":parameters, "timeout":time_out}
        request_fun = requests.get   
    try:
        return_result = request_fun(**fields)
        if return_result.status_code == 200:
            return_result = {"state":'ok'}
    except requests.exceptions.ConnectTimeout:
        return_result = {'state':'error', 'information':'connection time out'}
    except requests.exceptions.InvalidHeader:
        return_result = {'state':'error', 'information':'header error'}
    except requests.exceptions.ConnectionError:
        return_result = {'state':'error', 'information':'connection error'}
    
    return return_result


