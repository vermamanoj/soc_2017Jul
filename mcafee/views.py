import logging

from django.http import JsonResponse
from django.shortcuts import render

from . import mcafee_connector

logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)

def mcafee_system_list(request):
    command = 'system.find'
    parameter = ''
    system_list = mcafee_connector.get_mcafee_data(command, parameter)

    # return render(request, 'mcafee_systems_list.html', {'success' :system_list})
    return render(request, 'mcafee_systems_list.html', system_list)
    # return JsonResponse(system_list)


def mcafee_system_list_json(request):
    command = 'system.find'
    parameter = ''
    system_list = mcafee_connector.get_mcafee_data(command, parameter)
    print(system_list)
    # return render(request, 'mcafee_systems_list.html', {'success' :system_list})
    # return render(request, 'mcafee_systems_list.html', system_list)
    return JsonResponse(system_list)


def system_dat_json(request):
    from requests import Session

    try:
        from urlparse import urljoin
    except ImportError:
        from urllib.parse import urljoin

    # url = 'https://34.201.165.252:8443/remote/core.listQueries'
    url = 'https://34.201.165.252:8443/remote/core.executeQuery?target=EPOLeafNode&select=(select+EPOComputerProperties.ComputerName+EPOComputerProperties.DomainName+EPOComputerProperties.IPAddress+EPOLeafNode.Tags+EPOLeafNode.os+EPOLeafNode.LastUpdate+EPOProdPropsView_VIRUSCAN.productversion+EPOProdPropsView_VIRUSCAN.datver)'
    user = 'admin'
    password = 'McAfee_ePO_@dm1n'

    s = Session()
    s.verify = False
    s.auth = (user, password)

    r = s.get(url)
    dat_list = []
    dict_new = {}
    for x in r.iter_lines():

        # print(x.decode('utf-8'))
        try:
            key, value = (x.decode('utf-8')).split(":")
            dict_new[key] = value
        except:
            if x.decode('utf-8') == "":
                print("NULL")
                dat_list.append(dict_new)
                dict_new = {}

    dat_list
    result = {
        "success": dat_list
    }
    return JsonResponse(dat_list, safe=False)


def system_dat(request):
    return render(request, 'mcafee_systems_dat.html')

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
        # return render(request, 'mcafee_connector.html', result)
        return JsonResponse(result, )
