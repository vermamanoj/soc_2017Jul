import requests
from requests.auth import HTTPBasicAuth
import logging
import os
import sys
from configparser import ConfigParser
from gentelella.core import global_config


logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)

class XForceClient:

    def __init__(self,):
        self.key = self.get_config()['success']['key']
        self.password = self.get_config()['success']['password']

    def get_config(self):
        # The function does not take any input
        # The variable config_exists is used to verify if config was read properly or not
        # and its used to return error message if it remains False
        config_exists = 0
        # Call get_global_config function to read name and path of  credentials file
        global_configuration = global_config.get_global_config()
        if global_configuration['outcome'] == 'success':
            configFile = global_configuration['data']['credentials_file']
            try:
                if os.path.exists(configFile):
                    config = ConfigParser()
                    config.read(r'./config/config.ini')
                    print(config)
                    if 'xforce' in config.sections():
                        result = {
                            "outcome": "success",
                            "success": {"key": config['xforce']['API_Key'], "password": config['xforce']['API_Password']}
                        }
                        config_exists = 1
                        return result
            except:
                logger.error(sys.exc_info())
        if config_exists == 0:
            result = {
                "outcome": "error",
                "error": "Configuration does not exist"
            }
            return result


    def get_dns(self, domain="api.xforce.ibmcloud.com"):
        url = "https://api.xforce.ibmcloud.com/resolve/" + domain
        print(url)
        response = requests.get(url, auth=HTTPBasicAuth(self.key, self.password))
        return response.json()

    def get_xforce(self, endpoint, data):
        url = "https://api.xforce.ibmcloud.com/" + endpoint + "/" + data
        print(url)
        response = requests.get(url, auth=HTTPBasicAuth(self.key, self.password))
        return response.json()

