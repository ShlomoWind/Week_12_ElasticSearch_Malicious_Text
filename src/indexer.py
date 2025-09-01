import pandas as pd
from elasticsearch import helpers

class EsIndexer:
    def __init__(self,es,index_name,df):
        self.df =df
        self.es = es
        self.index_name = index_name

    def is_date_column(self, series):
        try:
            pd.to_datetime(series,format="%Y-%m-%d %H:%M:%S%z",errors='raise')
            return True
        except:
            return False

    def mapping(self):
        props = {}
        for col in self.df.columns:
            col_lower = col.lower()
            if 'id' in col_lower:
                props[col] = {"type": "keyword"}
            elif self.is_date_column(self.df[col]):
                props[col] = {"type": "date"}
            elif pd.api.types.is_bool_dtype(self.df[col]):
                props[col] = {"type": "boolean"}
            elif pd.api.types.is_integer_dtype(self.df[col]):
                props[col] = {"type": "integer"}
            elif pd.api.types.is_float_dtype(self.df[col]):
                props[col] = {"type": "float"}
            else:
                props[col] = {"type": "text"}
        print("finished the mapping")
        return {"mappings": {"properties": props}}

    def create_index(self):
        mapping = self.mapping()
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, body=mapping)
        print(f"Index '{self.index_name}' created with mapping.")

    def index_dataframe(self):
        actions = [
            {
                "_index": self.index_name,
                "_id": i,
                "_source": record
            }
            for i, record in enumerate(self.df.to_dict(orient="records"), 1)
        ]
        helpers.bulk(self.es, actions)
        print(f"{len(self.df)} docs indexed in bulk!")
        self.es.indices.refresh(index=self.index_name)