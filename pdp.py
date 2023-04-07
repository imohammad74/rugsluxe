import time

import requests
from bs4 import BeautifulSoup

from common import Common
from db import DBManagement as db
from pdp_elements import PDPElements
from table import PriceTable


class PDP:
    @staticmethod
    def main(data):
        url = data[0]
        brand = data[1]
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        if PDPElements.is_in_stock(soup):
            try:
                features = PDPElements().features_title(soup)
            except:
                features = []
            try:
                feature_values = PDPElements.feature_value(soup)
            except:
                feature_values = []
            try:
                variants = PriceTable.main(soup)
            except:
                variants = []
            try:
                title = PDPElements.title(soup)
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
                    size = PDPElements.shape_size(soup)[variants.index(variant)][0]
                except:
                    size = ''
                try:
                    shape = PDPElements.shape_size(soup)[variants.index(variant)][1]
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
                    {'column': 'sale_price', 'value': sale_price}
                ]
                try:
                    db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[2], columns=all_columns)
                    # print(all_columns)
                except:
                    db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[3],
                                   columns=[{'column': 'url', 'value': url}])
                    # print('error')
            print(f'"{title}" finish!')
        else:
            print('Product is out of stock')
            query = f'''INSERT INTO NoData (URLAddress, ErrorMsg) VALUES ('{url}', 'Out of stock')'''
            db.custom_query(db_file=db.db_file(), query=query)


    def __init__(self, data):
        time.sleep(2)
        self.main(data)
