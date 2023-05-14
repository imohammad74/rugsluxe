from datetime import datetime

from common import Common
from db import DBManagement as db

now = datetime.now()


class PriceCheckWithSource:
    @staticmethod
    def get_data(table_name: str, columns: list) -> list:
        source = db.fetch_datas(db_file=db.db_file(), table_name=table_name,
                                all_columns=False, columns=columns)
        for i in range(len(source)):
            my_tuple = source[i]
            for j in range(len(my_tuple)):
                source[i] = tuple(str(s).lower() for s in my_tuple if s is not None)
        return source

    def check_price(self):
        current_time = int(now.strftime("%y%m%d"))
        source_data = self.get_data(table_name=db.db_table()[7],
                                    columns=['CollectionName', 'DesignID', 'Size', 'Price', 'Brand', 'SKU', 'UPC'])
        select_data = self.get_data(table_name=db.db_table()[8],
                                    columns=['CollectionName', 'DesignID', 'SKU', 'Price', 'URL'])
        for select_item in select_data:
            select_sku = select_item[2]
            print(select_sku)
            for source_item in source_data:
                source_sku = source_item[5]
                if select_sku == source_sku:
                    try:
                        collection_name = select_item[0]
                        design_id = select_item[1]
                        size = Common.find_size(source_item[2])
                        source_price = source_item[3]
                        select_price = select_item[3]
                        brand = source_item[4]
                        url = select_item[4]
                        sku = select_sku
                        upc = source_item[6]
                        minus = float(float(select_price) - float(source_price))
                        minus = round(minus)
                    except IndexError:
                        source_price = ''
                        select_price = ''
                        minus = ''
                    columns = [
                        {'column': 'CrawlSource', 'value': 'RugsLuxe'},
                        {'column': 'upc', 'value': upc},
                        {'column': 'sku', 'value': sku},
                        {'column': 'LastUpdate', 'value': current_time},
                        {'column': 'BrandName', 'value': brand},
                        {'column': 'CollectionName', 'value': collection_name},
                        {'column': 'DesignId', 'value': design_id},
                        {'column': 'Size', 'value': size},
                        {'column': 'SourcePrice', 'value': source_price},
                        {'column': 'CrawlPrice', 'value': select_price},
                        {'column': 'URL', 'value': url},
                        {'column': 'IsWarning', 'value': minus}
                    ]
                    db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[5], columns=columns)
        db.custom_query(db_file=db.db_file(), query=Common.sql_replace(table_name=db.db_table()[5])[0])
        db.custom_query(db_file=db.db_file(), query=Common.sql_replace(table_name=db.db_table()[5])[1])
        db.custom_query(db_file=db.db_file(), query=Common.sql_replace(table_name=db.db_table()[5])[2])
        print('finish')
