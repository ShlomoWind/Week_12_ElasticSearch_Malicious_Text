from loader import CsvLoader
from es_connector import EsConnector
from indexer import EsIndexer
from sentiments import Sentiment
from weapons import Weapon
from elasticsearch import helpers
from deleter import DeleteData

class DataManager:
    def __init__(self, csv_path, es_host, index_name, weapons_file=None):
        self.csv_path = csv_path
        self.es_host = es_host
        self.index_name = index_name
        self.weapons_file = weapons_file

        self.loader = CsvLoader(self.csv_path)
        self.es_connector = EsConnector(self.es_host)
        self.df = None
        self.es = None
        self.indexer = None
        self.weapon_checker = Weapon(self.weapons_file, "") if self.weapons_file else None
        self.deleter = None

    def build_index(self):
        self.df = self.loader.load()
        print(f"Loaded {len(self.df)} rows")
        self.es = self.es_connector.connect()
        self.indexer = EsIndexer(self.es, self.index_name, self.df)
        self.indexer.create_index()
        self.indexer.index_dataframe()
        print("Initial indexing done!")
        self.deleter = DeleteData(self.es, self.index_name)

    def analyze_and_update(self):
        docs = self.es.search(index=self.index_name, query={"match_all": {}}, size=10000)
        actions = []
        for hit in docs['hits']['hits']:
            doc_id = hit['_id']
            text = hit['_source'].get("text", "")
            sentiment = Sentiment(text)
            sentiment_value = sentiment.sentiment_type()

            found = None
            if self.weapon_checker:
                self.weapon_checker.text = text
                found = self.weapon_checker.weapon_blacklist()

            actions.append({
                "_op_type": "update",
                "_index": self.index_name,
                "_id": doc_id,
                "doc": {
                    "Sentiment": sentiment_value,
                    "WeaponsFound": found
                }
            })

        helpers.bulk(self.es, actions)
        self.es.indices.refresh(index=self.index_name)
        print(f"Bulk analysis and updates completed for {len(actions)} documents!")

    def run(self):
        self.build_index()
        self.analyze_and_update()
        self.deleter.delete_not_malicious()