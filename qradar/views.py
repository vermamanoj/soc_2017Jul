import json
import logging

from django.http import JsonResponse
from django.shortcuts import render, redirect

from . import qradar_api_client, qradar_connector

logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


# Create your views here.
# Default function
def index(request):
    return render(request, "qradar_aql.html")

def qradar_config(request):
    data = qradar_connector.get_qradar_config()
    if data['outcome'] == 'error':

        return render(request, 'qradar_connector.html', data)
    else:
        result = {
                    "outcome":"success",
                    "success":{"host":data['success']['host'],
                               "port": data['success']['port'],
                               "username":data['success']['username']}
                    }
        return render(request, 'qradar_connector.html', result)

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
        return render(request, "qradar_aql.html", {"error": error_message})
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
        return render(request, "qradar_aql.html", {"success": result})
    else:
        return render(request, "qradar_aql.html", {"error": "Could not fetch data"})


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
                             {"data" : result,
                            "chart_type":"bar",
                              "x": "CategoryName"
                         },},
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
        print("Result size is " + str(result.__sizeof__()/1024) + "KB")
        #return render(request, "qradar_aql.html",{"success":result})
        response = {
            "outcome": "success",
            "success":
                        {"userBySourceIP":
                             {"data" : result,
                            "chart_type":"pie",
                         },
                         },
                    }
    else:
        response = {
            "outcome": "error",
            "error"  : "some error from function qradar_userBySourceIP"
                    }
    return JsonResponse(response, safe=False)

def qradar_dashboard1(request):
    dash1 = qradar_events_category(request)
    dash1 = json.loads(dash1.content.decode("utf-8"))
    print(dash1)
    dash1 = dash1['success']
    data = {"success": dash1}
    return render(request, 'qradar_dashboard1.html', data)