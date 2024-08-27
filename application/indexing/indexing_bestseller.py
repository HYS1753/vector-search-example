from gensim.models import Doc2Vec
import pandas as pd
from application.config.elasticsearch.es_helper import EsHelper


class IndexingBestseller:
    def __init__(self, index_name, model_path):
        self.es = EsHelper()
        self.index_name = index_name
        self.model_path = model_path

    def index_setting(self):
        index_name = self.index_name
        body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "description_vector": {
                        "type": "dense_vector",
                        "dims": 100
                    }
                }
            }
        }
        self.es.create_index(index_name, body)

    def nori_analyzer(self, text):
        token_list = self.es.get_analyzed_token("nori", text)
        return token_list

    def make_document_dataframe(self, excel_file_path):
        df = pd.read_excel(excel_file_path)
        # 데이터 전처리
        df = df.dropna(subset=["설명"])
        df["tokens"] = df["설명"].apply(self.nori_analyzer)
        data = {
            "seq": df["순위"],
            "isbn": df["ISBN"],
            "book_name": df["상품명"],
            "price": df["판매가"],
            "author": df["저자"],
            "publisher": df["출판사"],
            "description": df["설명"],
            "description_vector": df["tokens"]
        }
        return pd.DataFrame(data)

    def bulk_index(self, df):
        model = Doc2Vec.load(self.model_path)
        docs = [
            {
                '_index': self.index_name,
                '_source': {
                    'isbn': _row['isbn'],
                    'book_name': _row['book_name'],
                    'price': _row['price'],
                    'author': _row['author'],
                    'publisher': _row['publisher'],
                    'description': _row['description'],
                    'description_vector': model.infer_vector(_row['description_vector'])
                }
            }
            for _idx, _row in df.iterrows()
        ]
        self.es.bulk_insert(docs)


