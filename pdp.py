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
                variants = PriceTable(data).main(data)
            except:
                variants = []
            try:
                title = PDPElements.title(soup)[0]
            except:
                title = ''
            try:
                collection = PDPElements.collection(soup)
            except:
                collection = ''
            try:
                description = PDPElements.description(soup)
            except:
                description = ''
            try:
                design_id = PDPElements.design_id(soup)
            except:
                design_id = ''
            try:
                material = PDPElements.material(soup)
            except:
                material = ''
            try:
                weight = PDPElements.weight(soup)
            except:
                weight = ''
            try:
                pile_height = PDPElements.pile_height(soup)
            except:
                pile_height = ''
            try:
                country_manufacture = PDPElements.country_manufacture(soup)
            except:
                country_manufacture = ''
            try:
                ship_by = PDPElements.ship_by(soup)
            except:
                ship_by = ''
            try:
                clearance = PDPElements.clearance(soup)
            except:
                clearance = ''
            for variant in variants:
                try:
                    size = variant['size']
                except:
                    size = ''
                try:
                    shape = PDPElements.shape(soup)
                except:
                    shape = ''
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
                        {'column': 'material', 'value': material},
                        {'column': 'sale_price', 'value': sale_price},
                        {'column': 'collection', 'value': collection},
                        {'column': 'design_id', 'value': design_id},
                        {'column': 'sku', 'value': sku},
                        {'column': 'clearance', 'value': clearance},
                        {'column': 'ship_by', 'value': ship_by},
                        {'column': 'country_manufacture', 'value': country_manufacture},
                        {'column': 'pile_height', 'value': pile_height},
                        {'column': 'weight', 'value': weight}
                    ]

                    try:
                        db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[2], columns=all_columns)
                        db.update_rows(db_file=db.db_file(), table_name=db.db_table()[4],
                                       columns=[{'column': 'seq', 'value': i}], condition="name='URLs'")
                    except:
                        db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[3],
                                       columns=[{'column': 'url', 'value': url}])
                if category == 'pillow':
                    all_columns = [
                        {'column': 'Title', 'value': title},
                        {'column': 'Description', 'value': description},
                        {'column': 'URL', 'value': url},
                        {'column': 'SKU', 'value': sku},
                        {'column': 'Shape', 'value': shape},
                        {'column': 'Brand', 'value': brand},
                        {'column': 'CollectionName', 'value': collection},
                        {'column': 'DesignId', 'value': design_id},
                        {'column': 'Price', 'value': sale_price},
                        {'column': 'Size', 'value': size},
                        {'column': 'Material', 'value': material},
                        {'column': 'Clearance', 'value': clearance},
                        {'column': 'ShipBy', 'value': ship_by},
                        {'column': 'CountryManufacture', 'value': country_manufacture},
                        {'column': 'PileHeight', 'value': pile_height},
                        {'column': 'Weight', 'value': weight}
                    ]
                    try:
                        db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[8], columns=all_columns)
                        db.update_rows(db_file=db.db_file(), table_name=db.db_table()[4],
                                       columns=[{'column': 'seq', 'value': i}], condition="name='PillowURLs'")
                    except:
                        db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[3],
                                       columns=[{'column': 'url', 'value': url}])
            print(f'"{category} -> {title}" finish!')

    def __init__(self, params):
        self.main(params)
