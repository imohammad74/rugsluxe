import requests
from bs4 import BeautifulSoup

# from common import Common
from db import DBManagement as db
from get_all_brands_url import GetAllBrandsURL


class GetBrandsURL:

    @staticmethod
    def main(brand: dict):
        brand_name = brand["brand"]
        url = brand["url_address"]
        category = brand['category']
        print(f'start crawling {category} -> {brand_name}')
        re = requests.get(url)
        soup = BeautifulSoup(re.content, "html.parser")
        params = {
            'category': category,
            'brand': brand_name,
            'url': url,
            're': re,
            'soup': soup
        }
        GetAllBrandsURL(params=params)

    def __init__(self, category_name: str):
        # max_worker = Common.max_worker()
        brands_url = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[1], all_columns=True)
        for i in range(len(brands_url)):
            category = brands_url[i][0]
            brand = brands_url[i][2]
            url_address = brands_url[i][3]
            if category == category_name:
                brand = {'category': category, 'brand': brand, 'url_address': url_address}
                self.main(brand)
        # Worker(fn=self.main, data=brands, max_worker=max_worker)
