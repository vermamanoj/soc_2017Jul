#!/usr/bin/env python3


import logging
import os
import sys
from configparser import ConfigParser

from gentelella.core import global_config

logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


def get_mcafee_config():
    # The function does not take any input
    # In the output it sends URL, username and password of ServiceNow

    # The variable snow_config_exists is used to verify if config was read properly or not
    # and its used to return error message if it remains False
    mcafee_config_exists = 0

    # Call get_global_config function to read name and path of ServiceNow credentials file
    global_configuration = global_config.get_global_config()

    if global_configuration['outcome'] == 'success':
        configFile = global_configuration['data']['credentials_file']

        try:
            if os.path.exists(configFile):
                config = ConfigParser()
                config.read(r'./config/config.ini')
                print(config)
                if 'epo' in config.sections():

                    host = config['epo']['host']
                    port = config['epo']['port']
                    username = config['epo']['username']
                    password = config['epo']['password']


                result = {
                    "outcome":"success",
                    "success":{"host": host, "port":port, "username":username, "password":password}
                    }
                mcafee_config_exists = 1
                return result

        except:
            logger.error(sys.exc_info())

    if mcafee_config_exists == 0:
        result = {
            "outcome": "error",
            "error": "Configuration does not exist"
        }
        return result

# Implementation of McAfee Client
# After running this cell create a client using
#   client = Client(url, user, password)

# Then run McAfee ePO commands as argument to client object
# to run 'system.find" command, run
#   systems = client('system.find', '')

import json
from requests import Session

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class APIError(Exception):
    """Represents an error with the data received within a valid HTTP response."""

class McAfeeClient:
    """Communicate with an ePO server.
    Instances are callable, pass a command name and parameters to make API calls.
    """

    def __init__(self, url, username, password, session=None):

        self.url = url
        self.username = username
        self.password = password

        if session is None:
            session = Session()
            session.verify = False

        self._session = session
        self._token = None

    def _get_token(self, _skip=False):
        """Get the security token if it's not already cached.

        :param bool _skip: used internally when making the initial request to get the token
        """

        if self._token is None and not _skip:
            self._token = self._request('core.getSecurityToken')

        return self._token

    def _request(self, name, **kwargs):
        """Format the request and interpret the response.
        Usually you want to use :meth:`__call__` instead.

        :param name: command name to call
        :param kwargs: arguments passed to :meth:`requests.request`
        :return: deserialized JSON data
        """

        kwargs.setdefault('auth', (self.username, self.password))
        params = kwargs.setdefault('params', {})
        # check whether the response will be json (default)
        is_json = params.setdefault(':output', 'json') == 'json'
        # add the security token, unless this is the request to get the token
        params.setdefault('orion.user.security.token', self._get_token(_skip=name == 'core.getSecurityToken'))
        url = urljoin(self.url, 'remote/{}'.format(name))

        if kwargs.get('data') or kwargs.get('json') or kwargs.get('files'):
            # use post method if there is post data
            r = self._session.post(url, **kwargs)
        else:
            r = self._session.get(url, **kwargs)

        # check that there was a valid http response
        r.raise_for_status()
        text = r.text

        if not text.startswith('OK:'):
            # response body contains an error
            raise APIError(text)

        return json.loads(text[3:]) if is_json else text[3:]

    def __call__(self, name, *args, **kwargs):
        """Make an API call by calling this instance.
        Collects arguments and calls :meth:`_request`.

        ePO commands take positional and named arguments.  Positional arguments are internally numbered "param#" and
        passed as named arguments.

        Files can be passed to some commands.  Pass a dictionary of ``'filename': file-like objects``, or other formats
        accepted by :meth:`requests.request`.  This command will not open files, as it is better to manage that in a
        ``with`` block in calling code.

        :param str name: command name to call
        :param args: positional arguments to command
        :param kwargs: named arguments to command
        :param dict params: named arguments that are not valid Python names can be provided here
        :param dict files: files to upload to command
        :return: deserialized JSON data
        """

        params = kwargs.pop('params', {})
        files = kwargs.pop('files', {})

        for i, item in enumerate(args, start=1):
            params['param{}'.format(i)] = item

        params.update(kwargs)
        return self._request(name, params=params, files=files)

def get_mcafee_data(command = 'system.find', parameter = ''):
    epo_config = get_mcafee_config()
    if epo_config['outcome'] == 'success':
        host = epo_config['success']['host']
        port = epo_config['success']['port']
        username = epo_config['success']['username']
        password = epo_config['success']['password']
        url = "https://" + host + ":" + port

        try:
            mcafee_client = McAfeeClient(url, username, password)
            data = mcafee_client(command, parameter)

            list = []
            for system in data:
                dict = {}
                dict['ComputerName'] = system['EPOComputerProperties.ComputerName']
                dict['OS'] = system['EPOComputerProperties.OSType']
                list.append(dict)

            result = {
                "outcome": "success",
                "success": list

            }
            print(result)
            return result
        except:
            logger.error(sys.exc_info()[1])
            return {'outcome': 'error', 'error': sys.exc_info()[1]}
    else:
        result = {
            "outcome": "error",
            "error": "Configuration does not exist"
        }
        return result