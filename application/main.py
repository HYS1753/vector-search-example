import pandas as pd
from pecab import PeCab
import os
import requests, pandas
from application.common.path_utils import PathUtils

def pacab_test():
    pecab = PeCab()

    morphs = pecab.morphs("아버지가방에들어가시다.")
    print(morphs)

    srcPath = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    print(srcPath)

g_pathUtils = PathUtils(os.path.dirname(__file__))

# 교보문고
g_kyobo_best_seller_url = "https://store.kyobobook.co.kr/api/gw/best/file/downloads/excel?period=001&dsplDvsnCode=000&dsplTrgtDvsnCode=001&bestSeller=02"
# YES24
g_yes24_best_seller_url = "https://www.yes24.com/Product/Category/BestSellerExcel"
g_yes24_best_seller_data = {
    "bestType": "YES24_BESTSELLER",
    "categoryNumber": "001",
    "sex": "A",
    "age": "255",
    "pageNumber": "1",
    "pageSize": "5",
    "goodsStatGb": "06"
}

def main():
    response = requests.post(g_yes24_best_seller_url, data=g_yes24_best_seller_data)
    file_path = os.path.join(g_pathUtils.find_resource_dir(), "data", "yes24.xlsx")
    with open(file_path, "wb") as file:
        file.write(response.content)

    df = pd.read_excel(file_path)
    print(df)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()