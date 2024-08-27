import os.path

import pandas as pd
import time
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from application.common.path_utils import PathUtils
from application.config.elasticsearch.es_helper import EsHelper


class TrainingDoc2vec:
    def __init__(self, file_path):
        self.excel_file_path = file_path
        self.pre_proc_df = None
        self.tagged_data = None

    def verify_file_path(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    def nori_analyzer(self, text):
        es_helper = EsHelper()
        token_list = es_helper.get_analyzed_token("nori", text)
        return token_list

    # YES24 베스트 셀러 데이터 전처리
    def pre_proc_yes24(self):
        df = pd.read_excel(self.excel_file_path)
        # 데이터 전처리
        df = df.dropna(subset=["설명"])
        df["tokens"] = df["설명"].apply(self.nori_analyzer)
        data = {
            "seq": df["순위"],
            "description_vector": df["tokens"]
        }
        self.pre_proc_df = pd.DataFrame(data)
        return self.pre_proc_df

    def get_tagged_data(self):
        if self.pre_proc_df is None:
            raise ValueError(f"pre_proc_df not defined")
        document = self.pre_proc_df[["seq", "description_vector"]].values.tolist()
        self.tagged_data = [TaggedDocument(words=tokens, tags=[id]) for id, tokens in document]
        return self.tagged_data

    def doc2vec_training(self):
        self.pre_proc_yes24()
        self.get_tagged_data()

        max_epoch = 100
        model = Doc2Vec(
            window=3,           # 모델 학습 시 앞뒤로 보는 단어의 수
            vector_size=100,    # 백터 차원의 크기
            alpha=0.025,        # learning rate
            min_alpha=0.025,
            min_count=2,        # 학습에 사용할 최소 단어 빈도 수
            dm=0,               # 학습 방법 ( 0 = PV-DBOW, 1 = PV-DM )
            negative=5,         # Complexity Reduction
            seed=9999
        )

        # vocabulary 빌드
        model.build_vocab(self.tagged_data)

        # Doc2Vec training
        for epoch in range(max_epoch):
            start_time = time.time()
            model.train(self.tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.epochs)
            end_time = time.time()
            #print(f"{epoch} epoch duration time : {(end_time - start_time):.3f} sec.")

        path_utils = PathUtils(os.path.dirname(__file__))
        model_path = os.path.join(path_utils.find_resource_dir(), "model")
        self.verify_file_path(model_path)
        model_file_path = os.path.join(model_path, "doc2vec.model")
        model.save(model_file_path)
        return model_file_path

def main():
    tdv = TrainingDoc2vec("/Users/hy/git/vector-search-example/resource/data/yes24.xlsx")
    tdv.doc2vec_training()
    #tdv.pre_proc_yes24()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()