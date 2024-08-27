import pandas as pd
from gensim.models import Doc2Vec
from pecab import PeCab
import os

from application.config.elasticsearch.es_helper import EsHelper
from application.indexing.indexing_bestseller import IndexingBestseller
from application.pre_process.download_bestseller import DownloadBestSeller, CorpEnum
from application.common.path_utils import PathUtils
from application.pre_process.training_doc2vec import TrainingDoc2vec


def pacab_test():
    pecab = PeCab()

    morphs = pecab.morphs("아버지가방에들어가시다.")
    print(morphs)

    srcPath = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    print(srcPath)

g_pathUtils = PathUtils(os.path.dirname(__file__))

def indexing():
    # 0. file download
    downloader = DownloadBestSeller(type=CorpEnum.YES24)
    file_path = downloader.download()

    # 1. training doc2vec
    doc2vec = TrainingDoc2vec(file_path)
    model_path = doc2vec.doc2vec_training()

    # 2. indexing
    indexing = IndexingBestseller(index_name="bestseller", model_path=model_path)
    indexing.index_setting()
    doc = indexing.make_document_dataframe(file_path)
    indexing.bulk_index(doc)

def search():
    # Set model
    path_utils = PathUtils(os.path.dirname(__file__))
    model_path = os.path.join(path_utils.find_resource_dir(), "model", "doc2vec.model")
    model = Doc2Vec.load(model_path)

    # infer_vector
    es_helper = EsHelper()
    query = "고전 인문학"
    vector = model.infer_vector(es_helper.get_analyzed_token("nori", query))

    # search
    search_qeury = {
        "script_score": {
            "query": {
                "match_all": {}
            },
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'description_vector') + 1.0",
                "params": {
                    "query_vector": vector.tolist()
                }
            }
        }
    }
    print(search_qeury)
    response = es_helper.search(index="bestseller", query=search_qeury)
    print(response)
    hits = response["hits"]["hits"]
    for doc in hits:
        print(doc["_source"]["book_name"])
        print(doc["_source"]["description"])
        print("================================================================================================")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    search()