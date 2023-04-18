import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from db import DBManagement as db
from pdp_elements import PDPElements
from table import PriceTable


class PDP:
    @staticmethod
    def main(data):
        total_count = len(data)
        urls = [data[i][0] for i in range(total_count)]
        brands = [data[i][1] for i in range(total_count)]
        # r = requests.get(url)
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        for i in range(total_count):
            url = urls[i]
            brand = brands[i]
            driver.get(url)
            print(f'{i + 1} of {total_count} | {url}')
            time.sleep(0.5)
            data = driver.page_source
            soup = BeautifulSoup(data, 'html.parser')
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
                    # size = PDPElements.shape_size(soup)[variants.index(variant)][0]
                    size = variant['size']
                except:
                    size = ''
                try:
                    # shape = PDPElements.shape_size(soup)[variants.index(variant)][1]
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
        driver.quit()

    def __init__(self, data):
        self.main(data)
