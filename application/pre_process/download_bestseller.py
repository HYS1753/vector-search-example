import os.path

from application.common.path_utils import PathUtils
from enum import Enum, auto

import requests

# 교보문고
g_kyobo_best_seller_file_name = "kyobo.xlsx"
g_kyobo_best_seller_url = "https://store.kyobobook.co.kr/api/gw/best/file/downloads/excel?period=001&dsplDvsnCode=000&dsplTrgtDvsnCode=001&bestSeller=02"
# YES24
g_yes24_best_seller_file_name = "yes24.xlsx"
g_yes24_best_seller_url = "https://www.yes24.com/Product/Category/BestSellerExcel"
g_yes24_best_seller_data = {
    "bestType": "YES24_BESTSELLER",
    "categoryNumber": "001",
    "sex": "A",
    "age": "255",
    "pageNumber": "1",
    "pageSize": "500",
    "goodsStatGb": "06"
}

class CorpEnum(Enum):
    KYOBO = auto()
    YES24 = auto()

class DownloadBestSeller:
    def __init__(self, type=None, file_path=None):
        if type is None:
            self.corp = CorpEnum.KYOBO
        elif isinstance(type, CorpEnum):
            self.corp = type
        else:
            raise TypeError(f"Expected type 'CorpEnum', got {type.__class__.__name__}")

        if file_path is None:
            path_utils = PathUtils(os.path.dirname(__file__))
            self.file_path = os.path.join(path_utils.find_resource_dir(), "data")
        else:
            self.file_path = file_path

    def verify_file_path(self):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

    def download(self):
        file_path = ""
        try:
            self.verify_file_path()
            if self.corp == CorpEnum.KYOBO:
                response = requests.get(g_kyobo_best_seller_url)
                file_path = os.path.join(self.file_path, g_kyobo_best_seller_file_name)
            else:
                response = requests.post(g_yes24_best_seller_url, data=g_yes24_best_seller_data)
                file_path = os.path.join(self.file_path, g_yes24_best_seller_file_name)

            with open(file_path, "wb") as file:
                file.write(response.content)
        except Exception as e:
            print(f"download bestseller file failed: {e}")

        return file_path