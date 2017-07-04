from django.shortcuts import render
from . import snow
# Create your views here.

import logging
logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)

def servicenow(request, table = "incident", *arg):
    if arg:
        table = table
        sys_id = arg[0]
        operator = '/'
        data = snow.get_snow_data(table, operator,sys_id)
        logger.info(data)
        return render(request, 'snow.html', context={'data': data['success'], 'type': 'single'})
    else:
        operator = '?'
        fields = 'priority, short_description, incident_state, opened_by.name, \
            assignment_group.name, sys_created_on, assigned_to.name, number, category, sys_id'
        query =  'sysparm_fields=' + fields
        data = snow.get_snow_data(table, operator, query)
        logger.info('runing with arg=Flase')
        if data['outcome'] == 'error':
            return render(request, 'snow.html', context={'data':data})
        return render(request, 'snow.html', context={'data':data['success'], 'type': 'summary'})
