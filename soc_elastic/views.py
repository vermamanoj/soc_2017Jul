from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from elasticsearch import Elasticsearch

# Create your views here.
def index(request):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    result = es.search(index="test", body={"size":50, "query": {"match_all": {}}})
    result = result['hits']['hits']
    return JsonResponse(result, safe=False)

def show_siem_alerts(request):
    return render(request, 'offenses_from_elastic.html')