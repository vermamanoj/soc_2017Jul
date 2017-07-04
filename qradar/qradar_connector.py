#!/usr/bin/env python3


import os
import sys
import requests
from configparser import ConfigParser
from gentelella.core import global_config

import logging
logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)

def get_qradar_config():
    # The function does not take any input
    # In the output it sends URL, username and password of ServiceNow

    # The variable snow_config_exists is used to verify if config was read properly or not
    # and its used to return error message if it remains False
    qradar_config_exists = 0

    # Call get_global_config function to read name and path of ServiceNow credentials file
    global_configuration = global_config.get_global_config()

    if global_configuration['outcome'] == 'success':
        configFile = global_configuration['data']['credentials_file']
        logger.warning(configFile)

        try:
            if os.path.exists(configFile):
                config = ConfigParser()
                config.read(r'./config/config.ini')
                print(config)
                if 'qradar' in config.sections():
                    logger.warning("Qradar config exists..................")

                    host = config['qradar']['host']
                    port = config['qradar']['port']
                    username = config['qradar']['username']
                    password = config['qradar']['password']


                result = {
                    "outcome":"success",
                    "success":{"host": host, "port":port, "username":username, "password":password}
                    }
                qradar_config_exists = 1
                return result

        except:
            logger.error(sys.exc_info())

    if qradar_config_exists == 0:
        result = {
            "outcome": "error",
            "error": "Configuration does not exist"
        }
        return result
