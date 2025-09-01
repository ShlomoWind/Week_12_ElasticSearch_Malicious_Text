import time
from elasticsearch import Elasticsearch

class EsConnector:
    def __init__(self,host):
        self.es = None
        self.host = host

    def connect(self):
        for i in range(10):
            try:
                self.es = Elasticsearch(self.host, request_timeout=30)
                if self.es.ping():
                    print("Elasticsearch is ready!")
                    break
            except Exception:
                print("Waiting for Elasticsearch...")
                time.sleep(3)