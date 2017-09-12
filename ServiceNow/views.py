import logging
import re

from django.shortcuts import render

from . import snow

logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


# def servicenow(request, table = "incident", *arg):
def servicenow(request, table="incident", *arg):
    if arg:
        table = table
        sys_id = arg[0]
        operator = '/'
        data = snow.get_snow_data(table, operator,sys_id)
        logger.info(data)
        return render(request, 'snow.html', context={'data': data, 'type': 'single'})
    else:
        operator = '?'
        fields = 'priority, short_description, incident_state, opened_by.name, \
            assignment_group.name, sys_created_on, assigned_to.name, number, category, sys_id'
        query =  'sysparm_fields=' + fields
        data = snow.get_snow_data(table, operator, query)
        logger.info(data)

        if data['outcome'] == 'error':
            return render(request, 'snow.html', context={'data':data})

        # remove dot (.) from key name
        new_list = []
        for r in data['success']['result']:
            new_dict = {}
            for key, value in r.items():
                key = re.sub(r"\.", "", key)
                new_dict[key] = value
                print(new_dict)
            new_list.append(new_dict)
        result = {
            "outcome": "success",
            "success": {
                "result": new_list
            }
        }
        logger.info(result)
        return render(request, 'snow.html', context={'data': result, 'type': 'summary'})
