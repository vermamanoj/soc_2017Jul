from django.shortcuts import render
from configparser import ConfigParser
from gentelella.core import global_config
import os
from . import mcafee_connector
import json

# Create your views here.

import logging
logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)

def mcafee_system_list(request):
    command = 'system.find'
    parameter = ''
    system_list = mcafee_connector.get_mcafee_data(command, parameter)

    return render(request, 'mcafee_systems_list.html', system_list)

def mcafee_config(request):
    data = mcafee_connector.get_mcafee_config()
    if data['outcome'] == 'error':
        return render(request, 'mcafee_connector.html', data)
    else:
        result = {
                    "outcome":"success",
                    "success":{"host":data['success']['host'],
                               "port": data['success']['port'],
                               "username":data['success']['username']}
                    }
        return render(request, 'mcafee_connector.html', result)

