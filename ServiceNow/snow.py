#!/usr/bin/env python3
#ServiceNow


import logging
import os
import sys
from configparser import ConfigParser

import requests

from gentelella.core import global_config

logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


def get_snow_config():
    # The function does not take any input
    # In the output it sends URL, username and password of ServiceNow

    # The variable snow_config_exists is used to verify if config was read properly or not
    # and its used to return error message if it remains False
    snow_config_exists = 0

    # Call get_global_config funvtion to read name and path of ServiceNow credentials file
    global_configuration = global_config.get_global_config()

    if global_configuration['outcome'] == 'success':
        configFile = global_configuration['data']['credentials_file']

        try:
            if os.path.exists(configFile):
                config = ConfigParser()
                config.read(r'./config/config.ini')
                print(config)
                if 'snow' in config.sections():

                    url = "https://" + config['snow']['host'] + "/api/now/"
                    username = config['snow']['username']
                    password = config['snow']['password']

                result = {
                    "outcome":"success",
                    "success":{"url":url, "username":username, "password":password}
                    }
                snow_config_exists = 1
                return result

        except:
            logger.error(sys.exc_info())

    if snow_config_exists == 0:
        result = {
            "outcome": "error",
            "error": "Configuration does not exist"
        }
        return result


# def get_snow_data(table='incident',*arg):

def get_snow_data(table='sn_si_incident', *arg):
    # Set the request parameters
    # URL format - 'https://dev24263.service-now.com/api/now/'

    snow_config = get_snow_config()
    if snow_config['outcome'] == 'success':
        baseurl = snow_config['success']['url']
        username = snow_config['success']['username']
        password  = snow_config['success']['password']

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # ------------------------
        # Do the HTTP request
        if arg:
            url = baseurl + 'table/' + table + arg[0] + arg[1]
            logger.info(url)
        else:
            url = baseurl + 'table/' + table
            logger.info(url)
        try:
            response = requests.get(url, auth=(username, password), headers=headers)
            # Check for HTTP codes other than 200
            if response.status_code != 200:
                return {'outcome':'error', 'Status': response.status_code, 'Headers': response.headers, 'error': response.json(),
                }

            if "Hibernating" in response.content.decode('utf-8'):
                error_msg = "ServiceNow instance is in Hibernate mode, please wake it up by visiting " + baseurl
                return {'outcome': 'error',
                        'error': error_msg,
                        }

            # Decode the JSON response into a dictionary and use the data
            data = {'outcome': 'success', 'success': response.json()}
            print(data)
            return (data)
        except:
            logger.error(sys.exc_info())
            return {'outcome':'error', 'error': sys.exc_info()}

    else:
        result = {
            "outcome": "error",
            "error": "Configuration does not exist"
        }
        return result





