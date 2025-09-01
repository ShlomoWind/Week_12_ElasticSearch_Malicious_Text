class DeleteData:
    def __init__(self, es, index_name):
        self.es = es
        self.index_name = index_name

    def delete_not_malicious(self):
        query = {
            "query": {
                "bool": {
                    "must_not": [
                        {"match": {"Classification": "antisemitic"}},  # מסווג כאנטישמי
                        {"exists": {"field": "WeaponsFound"}}
                    ],
                    "should": [
                        {"term": {"Sentiment": "neutral"}},
                        {"term": {"Sentiment": "positive"}}
                    ],
                    "minimum_should_match": 1
                }
            }
        }
        res = self.es.delete_by_query(index=self.index_name, body=query)
        self.es.indices.refresh(index=self.index_name)
        print(f"Deleted {res['deleted']} non-malicious documents.")