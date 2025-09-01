import time
from config.settings import ES_HOST
from elasticsearch import Elasticsearch

class EsConnector:
    def __init__(self):
        self.es = None

    def connect(self):
        for i in range(10):
            try:
                self.es = Elasticsearch(ES_HOST, request_timeout=30)
                if self.es.ping():
                    print("Elasticsearch is ready!")
                    break
            except Exception:
                print("Waiting for Elasticsearch...")
                time.sleep(3)