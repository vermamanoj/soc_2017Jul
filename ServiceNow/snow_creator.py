import sys, requests, json
from ServiceNow.models import Snow

def get_cust_details(cid):
        try:
            details = Snow.objects.get(uid=cid)
            return details
        except:
            error = sys.exc_info()[1]
            return "Error Connecting DB." + str(error) + "\n"

def create_inc(details):
    cudetails = get_cust_details(details['cid'])
    headers = {"Content-Type": "application/xml", "Accept": "application/json"}
    url = cudetails.base_url+ '/table/' + cudetails.table
    response = requests.get(url, auth=(cudetails.user, cudetails.pwd), headers=headers)

    if response.status_code is 200 or response.status_code is 201:
        url=url+ '?' + cudetails.fields
        #incdetails = "{'caller_id':'SOCAPI','category':'"+details['category']+"','subcategory':'"+details['sub_category']+"','state':'"+details['state']+"','impact':'"+details['impact']+"','urgency':'"+details['urgency']+"','assignment_group':'soc','short_description':'"+details['short_dis']+"','work_notes':'"+details['dis']+"'}"
        incdetails = "<request><entry><short_description>"+details['short_dis']+"</short_description><assignment_group>SOC</assignment_group><urgency>"+details['urgency']+"</urgency><impact>"+details['impact']+"</impact><caller_id>SOCAPI</caller_id><work_notes>"+details['dis']+"</work_notes><subcategory>"+details['sub_category']+"</subcategory><category>"+details['category']+"</category><state>"+details['state']+"</state></entry></request>"

        response = requests.post(url, auth=(cudetails.user, cudetails.pwd), headers=headers, data=incdetails)
        data = response.json()
        if 'status' in data.keys():
            if data['status'] == "failure":
                return "There Is An Error Creating Incident." + data['error']['message']+"\n\r"+data['error']['detail']
        elif 'result' in data.keys():
            db_outcome = save_inc(data,cudetails.uid)
            if 'result' in db_outcome.keys():
                return "Incident Created. Incident Number: " + str(data['result']['number']) + "<br><br>DB Status: " + db_outcome['result']
            else:
                return "Incident Created. Incident Number: " + str(data['result']['number'])+ "<br><br>DB Status: Error. Please Contact Administrator."
        else:
            return "Unexpected Error: Please Contact Administrator."
    else:
        return "Communication Error. Unable to Establish Connection With Remote Snow. Error Code: " + str(response.status_code)

def save_inc(incdata,cust_uid):
    from elasticsearch import Elasticsearch
    #from elasticsearch import exceptions as es_exceptions

    try:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except:
        error = sys.exc_info()[1]
        return "Error Connecting DB." + str(error) + "\n"
    # Write to Elasticsearch
    #print(incdata)
    try:
        incdata['result']['cust_id'] = cust_uid
        outcome = es.index(index='testinc', doc_type='incidents', body=incdata['result'])
    except:
        error = sys.exc_info()[1]
        return "Error Connecting DB." + str(error) + "\n"

    return outcome

