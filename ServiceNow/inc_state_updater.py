import sys, requests
from ServiceNow.models import Snow
from ServiceNow.snow_creator import get_cust_details

def get_snow_cust():
    try:
        customer_uid = {}
        i = 0
        for e in Snow.objects.all():
            customer_uid['customer_' + str(i)] = e.uid
            i = i + 1
        if 'customer_0' in customer_uid.keys():
            outcome = get_incidents(customer_uid)
            print(outcome)
            return outcome
        else:
            return "No Customer Details Found In DB. Please Contact Administrator."
    except:
        error = sys.exc_info()[1]
        return "Error Connecting DB." + str(error)

def get_incidents(customer_uid):
    from elasticsearch import Elasticsearch
    customer_uid = customer_uid['customer_0']
#Connection to ElasticSearch DB.

    try:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except:
        error = sys.exc_info()[1]
        return "Error Connecting DB." + str(error)

#Search Incidents, other than closed & resolved, in DB for first customer.

    try:
        res = es.search(index="testinc", doc_type='incidents', body={
            "query": {
                "bool": {
                    "must_not": [
                        {
                            "match": {
                                "state": "Closed"
                            }
                        },
                        {
                            "match": {
                                "state": "Resolved"
                            }
                        }
                    ]
                }
            }
        })
        print("KEYS")
        print(res['hits'].keys())
        if 'total' in res['hits'].keys():
            # inc_count = res['hits']['total']
            # if inc_count == 0:
            #     return "Nothing to update"
            # else:
            #     incidents = {}
            #     i = 0
            #     for inc in res['hits']['hits']:
            #         incidents['number'+str(i)] = inc['_source']['number']
            #         i = i+1
            #     outcome = get_status(incidents,customer_uid)
            #     return str(inc_count) + " Incidents to be updated" + "<br><br>Incident numbers: " + str(incidents)

            print("inside fucntion")
            incidents = []
            print(res)
            for record in res['hits']['hits']:
                print("looping")
                incidents.append({"es_id":record['_id'], "inc_no":record['_source']['number']})
            print("INCIDENTS")
            print(incidents)
            return incidents



        elif 'error' in res.keys():
            return res['error']['root_cause']
        else:
            return "Error: Please Contact Administrator."
        return res
    except:
        error = sys.exc_info()[1]
        return str(error)

def get_status(incidents,customer_uid):
    snow_details = get_cust_details(customer_uid)

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    try:
        url = snow_details.base_url + '/table/' + snow_details.table
        response = requests.get(url, auth=(snow_details.user, snow_details.pwd), headers=headers)
    except:
        error = sys.exc_info()[1]
        return str(error)

    if response.status_code is 200:
        data = response.json()
        if 'status' in data.keys():
            if data['status'] == "failure":
                return "There Is An Error Reading Incident." + "<br><br>Error: " + data['error']['message'] + "<br>Error Message: " + data['error']['detail']
        elif 'result' in data.keys():

            for x in incidents:
                fields = "?sysparm_query=number%3D" + x['inc_no'] + "&sysparm_display_value=true&sysparm_exclude_reference_link=true&sysparm_fields=number%2Cstate%2Cassignment_group"
                url = snow_details.base_url + '/table/' + snow_details.table + fields
                response = requests.get(url, auth=(snow_details.user, snow_details.pwd), headers=headers)
                data = response.json()
            # counter = 0
            # while counter < len(incidents):
            #     #print(incidents['number' + str(counter)])
            #     fields = "?sysparm_query=number%3D" + incidents['number' + str(counter)] + "&sysparm_display_value=true&sysparm_exclude_reference_link=true&sysparm_fields=number%2Cstate%2Cassignment_group"
            #     url = snow_details.base_url + '/table/' + snow_details.table + fields

                # response = requests.get(url, auth=(snow_details.user, snow_details.pwd), headers=headers)
                # data = response.json()
                # counter = counter + 1
        else:
            return "Error Getting Data From Snow."
    else:
        print("Error: "+str(response.status_code))

    print (snow_details)
    return "thanks"

if __name__ == '__main__':
    a = get_snow_cust()
    print (a)