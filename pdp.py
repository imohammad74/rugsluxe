import requests
from bs4 import BeautifulSoup

from db import DBManagement as db
from pdp_elements import PDPElements
from table import PriceTable


class PDP:
    @staticmethod
    def main(params):
        start_point = params['start_point']
        total_count = params['total_urls']
        urls = [params['data'][i][0] for i in range(total_count)]
        brands = [params['data'][i][1] for i in range(total_count)]
        categories = [params['data'][i][2] for i in range(total_count)]
        for i in range(start_point, total_count):
            url = urls[i]
            brand = brands[i]
            category = categories[i]
            r = requests.get(url)
            print(f'{i + 1} of {total_count} | {url}')
            soup = BeautifulSoup(r.content, 'html.parser')
            data = {'category': category, 'data': soup}
            try:
                features = PDPElements().features_title(soup)
            except:
                features = []
            try:
                feature_values = PDPElements.feature_value(soup)
            except:
                feature_values = []
            try:
                variants = PriceTable(data).main(data)
            except:
                variants = []
            try:
                title = PDPElements.title(soup)[0]
            except:
                title = ''
            try:
                collection = PDPElements().collection(soup)
            except:
                collection = ''
            try:
                description = PDPElements.description(soup)
            except:
                description = ''
            try:
                design_id = PDPElements().design_id(soup)
            except:
                design_id = ''
            try:
                construction = feature_values[(features.index('Construction'))]
            except:
                construction = ''
            try:
                material = feature_values[(features.index('Material'))]
            except:
                material = ''
            for variant in variants:
                try:
                    size = variant['size']
                except:
                    size = ''
                try:
                    shape = variant['shape']
                except:
                    shape = ''
                try:
                    msrp = variant['msrp']
                except:
                    msrp = ''
                try:
                    sale_price = variant['price']
                except:
                    sale_price = ''
                try:
                    sku = variant['sku']
                except:
                    sku = ''
                if category == 'rug':
                    all_columns = [
                        {'column': 'title', 'value': title},
                        {'column': 'description', 'value': description},
                        {'column': 'url', 'value': url},
                        {'column': 'size', 'value': size},
                        {'column': 'shape', 'value': shape},
                        {'column': 'brand', 'value': brand},
                        {'column': 'weave', 'value': construction},
                        {'column': 'material', 'value': material},
                        {'column': 'msrp', 'value': msrp},
                        {'column': 'collection', 'value': collection},
                        {'column': 'design_id', 'value': design_id},
                        {'column': 'sku', 'value': sku},
                        {'column': 'sale_price', 'value': sale_price}
                    ]

                    try:
                        db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[2], columns=all_columns)
                        db.update_rows(db_file=db.db_file(), table_name=db.db_table()[4],
                                       columns=[{'column': 'seq', 'value': i}], condition="name='URLs'")
                        if category == 'pillow':
                            db.update_rows(db_file=db.db_file(), table_name=db.db_table()[4],
                                           columns=[{'column': 'seq', 'value': i}], condition="name='PillowURLs'")
                        # print(all_columns)
                    except:
                        db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[3],
                                       columns=[{'column': 'url', 'value': url}])
                        # print('error')
                if category == 'pillow':
                    all_columns = [
                        {'column': 'Title', 'value': title},
                        {'column': 'URL', 'value': url},
                        {'column': 'SKU', 'value': sku},
                        {'column': 'Shape', 'value': shape},
                        {'column': 'Brand', 'value': brand},
                        {'column': 'CollectionName', 'value': collection},
                        {'column': 'DesignId', 'value': design_id},
                        {'column': 'Price', 'value': sale_price}
                    ]
                    print(all_columns)
                    try:
                        db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[8], columns=all_columns)
                        db.update_rows(db_file=db.db_file(), table_name=db.db_table()[4],
                                       columns=[{'column': 'seq', 'value': i}], condition="name='PillowURLs'")
                        # print(all_columns)
                    except:
                        db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[3],
                                       columns=[{'column': 'url', 'value': url}])
                        # print('error')
            print(f'"{category} -> {title}" finish!')
        # driver.quit()

    def __init__(self, params):
        self.main(params)
