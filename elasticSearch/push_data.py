from elasticsearch import Elasticsearch

from config import HOST, PORT


es_host = [{"host": HOST, "port": PORT}]
es = Elasticsearch(es_host)


class ElasticSearch:
    def __init__(self, host=es_host):
        self.host = host

    def push_msg(self, index, id, msg):
        """
        Push message to elasticsearch

        Args:
            index ([type]): index name
            id : id of message in index
            msg : message
        """
        es = Elasticsearch(self.host)
        es.index(index=index, id=id, msg=msg)
