import json
import logging

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .xforce import XForceClient

from . import qradar_api_client, qradar_connector

logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


# Create your views here.
# Default function
def index(request):
    return render(request, "qradar/qradar_aql.html")


def qradar_config(request):
    data = qradar_connector.get_qradar_config()
    if data['outcome'] == 'error':

        return render(request, 'qradar/qradar_connector.html', data)
    else:
        result = {
            "outcome": "success",
            "success": {"host": data['success']['host'],
                        "port": data['success']['port'],
                        "username": data['success']['username']}
        }
        return render(request, 'qradar/qradar_connector.html', result)


def run_aql_query(request, *query):
    print(request)
    if request.method == 'GET':
        print("redirecting to /qradar")
        return redirect('/qradar')
    logger.info((request.POST['aql_query']))
    search_id = qradar_api_client.q_create_search(request.POST['aql_query'])
    logger.info(search_id)
    if "error" in search_id.keys():
        error_message = search_id['error']
        logger.info(search_id['error'])
        return render(request, "qradar/qradar_aql.html", {"error": error_message})
    id = search_id['success']
    logger.info(id)
    res = qradar_api_client.q_search_result_ready(id)
    logger.info("resposne receivced from q_search_result_ready")
    logger.info(res)
    if "success" in res.keys():
        result = qradar_api_client.q_get_searches_result(id)
        # as result is in format {'events': []}, sending actual value only
        result = result['success']['events']
        print("Result size is " + str(result.__sizeof__() / 1024) + "KB")
        return render(request, "qradar/qradar_aql.html", {"success": result})
    else:
        return render(request, "qradar/qradar_aql.html", {"error": "Could not fetch data"})


def qradar_events_category(request):
    aql_query = "SELECT count(*), CATEGORYNAME(category) AS CategoryName \
      FROM events \
      WHERE hasoffense=TRUE \
      GROUP BY category \
      LAST 2 DAYS"
    search_id = qradar_api_client.q_create_search(aql_query)
    id = search_id['success']
    search_status = qradar_api_client.q_search_result_ready(id)
    print("Search status = " + str(search_status))
    if "error" in search_status.keys():
        return JsonResponse(search_status)
    if search_status['success'] == id:
        result = qradar_api_client.q_get_searches_result(id)
        # as result is in format {'events': []}, sending actual value only
        result = result['success']['events']
        print(result)
        print("Result size is " + str(result.__sizeof__() / 1024) + "KB")
        # return render(request, "qradar_aql.html",{"success":result})
        response = {"success":
                        {"events_by_category":
                             {"data": result,
                              "chart_type": "bar",
                              "x": "CategoryName"
                              }, },
                    }
    else:
        response = {"error":
                        "some error from fucntion qradar_events_category "
                    }
    return JsonResponse(response, safe=False)


def qradar_userBySourceIP(request):
    aql_query = "select username, UNIQUECOUNT(sourceip) as count_sourceip, \
        count(*) from events \
        group by username ORDER BY count_sourceip DESC  last 10 DAYS"
    search_id = qradar_api_client.q_create_search(aql_query)
    id = search_id['success']
    search_status = qradar_api_client.q_search_result_ready(id)
    if "error" in search_status.keys():
        return {search_status}
    if search_status['success'] == id:
        result = qradar_api_client.q_get_searches_result(id)
        # as result is in format {'events': []}, sending actual value only
        result = result['success']['events']
        print("Result size is " + str(result.__sizeof__() / 1024) + "KB")
        # return render(request, "qradar_aql.html",{"success":result})
        response = {
            "outcome": "success",
            "success":
                {"userBySourceIP":
                     {"data": result,
                      "chart_type": "pie",
                      },
                 },
        }
    else:
        response = {
            "outcome": "error",
            "error": "some error from function qradar_userBySourceIP"
        }
    return JsonResponse(response, safe=False)


def qradar_dashboard1(request):
    dash1 = qradar_events_category(request)
    dash1 = json.loads(dash1.content.decode("utf-8"))
    print(dash1)
    dash1 = dash1['success']
    data = {"success": dash1}
    return render(request, 'qradar/qradar_dashboard1.html', data)


'''
Funtion "get_offenses" takes returns one or more offenses based on query
this is not being used anywhere yet
'''


def get_offenses(request, id=None, siem_id=None, query=None):
    print(request)
    print(id)
    endpoint = '/siem/offenses'
    if id:
        endpoint = '/siem/offenses/' + str(id)
    # sends a POST request to https://<server_ip>/rest/api/ariel/searches

    try:
        if query:
            search_results = qradar_api_client.q_apiclient(endpoint, query)
        else:
            search_results = qradar_api_client.q_apiclient(endpoint)
    except:
        raise
        # if there is a problem, return error
    print(search_results)
    return JsonResponse({"success": search_results})


# "write_offenses_to_es"
# Author: MKV
# Created data: 07-Oct-2017
# Summary
#    collects offenses from QRadar and writes to ElasticSearch
# How does it works
#   1) Look for all offenses in QRadar
#   2) Write these offenses to ES with some additional fields
# Caller
#   1) runs on schedule.
# Output
#   Temporary meaningless output as of ow
def write_offenses_to_es(requests):
    from elasticsearch import Elasticsearch
    es = Elasticsearch([{'host': '172.16.0.29', 'port': 9200}])

    # es_write_outcome = es.index(index='qradar_offenses', doc_type='qradar_offenses', body=offense_data)
    es_query_match_all = '{"query":{"match_all":{}}}'
    es_response = es.search('qradar_offenses', body=es_query_match_all)
    es_offenses = es_response['hits']['hits']
    print(es_response)

    if len(es_offenses) > 0:
        print("records exist in the index")
        es_response = es.count('qradar_offenses', body=es_query_match_all)
        print("Totoal number of offenses = " + str(es_response['count']))
        return JsonResponse(es_response)

    else:
        print("No offense exists in Elasticsearch, queying from Qradar..")
        print("--------------------------------------------")
        offense_data = get_offenses(requests)
        data = json.loads((offense_data.content.decode('utf-8')))
        for offense in data['success']:
            es_write_outcome = es.index(index='qradar_offenses', doc_type='qradar_offenses', body=offense)
            print(es_write_outcome)
        return JsonResponse(es_write_outcome)
        # In order to allow non-dict objects to be serialized set the safe parameter to False in JsonResponse call.
        # return JsonResponse(data['success'], safe=False)


# "write_qradar_events_to_es"
# Summary
#    collects events from QRadar and writes to ElasticSearch
# How does it works
#   1) It will look for all offenses in ES with field "is_event_collected" == False
#   2) Fetch related events from QRadar
#   3) Write these events to ES with some additional fields
# Caller
#   1) runs on schedule.
#   2) Called by write_offense_to_es function
# Output
#   Returns json formatted list of dictionaries - offense_id and number of events written to ES
#   [{"offense_id":42, "num_events":99},]

def write_qradar_events_to_es(requests):
    from elasticsearch import Elasticsearch
    es = Elasticsearch([{'host': '172.16.0.29', 'port': 9200}])

    # es_write_outcome = es.index(index='qradar_offenses', doc_type='qradar_offenses', body=offense_data)
    es_query_match_all = '{"size":100,"query":{"match_all":{}}}'
    es_response = es.search('qradar_offenses', body=es_query_match_all)
    es_offenses = es_response['hits']['hits']
    offense_event_summary = []
    for offense in es_offenses:
        offense_id = offense["_source"]["id"]
        print(offense_id)
        aql_query = 'select QIDNAME(qid), CATEGORYNAME(highlevelcategory), CATEGORYNAME(category), LOGSOURCENAME(logsourceid), severity, sourceip, destinationip, "Filename",  username, domainid, UTF8(payload) from events where INOFFENSE(' + str(
            offense_id) + ') LAST 30 DAYS'
        # LAST 20 DAYS '

        print(aql_query)
        search_id = qradar_api_client.q_create_search(aql_query)
        id = search_id['success']
        search_status = qradar_api_client.q_search_result_ready(id)
        print("Search status = " + str(search_status))
        if "error" in search_status.keys():
            return JsonResponse(search_status)
        if search_status['success'] == id:
            result = qradar_api_client.q_get_searches_result(id)
            # as result is in format {'events': []}, sending actual value only

            result = result['success']['events']
            offense_event_summary.append({"offense_id": offense_id, "num_events": len(result)})
            for events in result:
                events['qradar_offense_id'] = offense_id
                es.index('qradar_events', doc_type='qradar_events', body=events)

            print("Result for offense id" + str(offense_id))
            print("Result size is " + str(result.__sizeof__() / 1024) + "KB")

            # return render(request, "qradar_aql.html",{"success":result})
        else:
            print("Error getting data for offense _id - " + str(offense_id))
    return JsonResponse({"success": offense_event_summary})


def get_es_offenses(requests, id=None):
    """
    :param requests:
    :return:
    """
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import Search
    try:
        es = Elasticsearch([{'host': '172.16.0.29', 'port': 9200}])
        if id:
            s = Search(using=es, index='qradar_offenses').query("match",id=id)
        else:
            s = Search(using=es, index='qradar_offenses').query("match_all")
        es_response = s.execute()
        # s = Search(using=es, index='qradar_offenses').query("match",device_count=2)
        # es_query_match_all = '{"query":{"match_all":{}}}'
        # es_response = es.search('qradar_offenses', body=es_query_match_all)
        #print(es_response)
        result = {
            "outcome": "success",
            "success": es_response.hits.hits
        }
        return JsonResponse(result, safe=False)
    except:
        result = {
            "outcome": "error",
            "error": "Some error occurred"
        }
        return JsonResponse(result, safe=False)




def show_alerts(request):
    '''
    the template calls get_es_offenses url to get json data
    :param request:
    :return:
    '''
    return render(request,"qradar_offense.html")

def xf_dns(request):
    '''
    the template calls get_es_offenses url to get json data
    :param request:
    :return:
    '''
    xfc = XForceClient()
    dns_result = xfc.get_dns("www.google.com")
    return JsonResponse(dns_result, safe=False)
