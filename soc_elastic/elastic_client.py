from django.http import JsonResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class ESClient:
    def __init__(self):
        # This code should later be changed to fetch URL and credentials from database
        self.host = 'localhost'
        self.port = 9200
        self.index_alerts = 'qradar_offenses'
        self.index_events = 'qradar_events'

    def get_alerts(self, id=None):
        """
        :param: id
        :return: all or few offenses
        """
        try:
            es = Elasticsearch([{'host': self.host, 'port': self.port}])
            if id:
                s = Search(using=es, index=self.index_alerts).query("match", id=id)
            else:
                s = Search(using=es, index='qradar_offenses').query("match_all")
            es_response = s.execute()

            # The following code accepts Elasticsearch DSL query format
            # es_query_match_all = '{"query":{"match_all":{}}}'
            # es_response = es.search('qradar_offenses', body=es_query_match_all)

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
