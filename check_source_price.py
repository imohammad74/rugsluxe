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
                # source[i] = tuple(my_tuple[k].lower()for k in range(len(my_tuple) - 1) if k is not None)
                source[i] = tuple(str(s).lower() for s in my_tuple if s is not None)
        return source

    def check_price(self):
        current_time = int(now.strftime("%y%m%d"))
        source_data = self.get_data(table_name=db.db_table()[7],
                                    columns=['CollectionName', 'DesignID', 'Size', 'Price', 'Brand', 'sku', 'UPC'])
        select_data = self.get_data(table_name=db.db_table()[2],
                                    columns=['collection', 'design_id', 'sku', 'sale_price'])
        source_collection = set(source_data[i][0] for i in range(len(source_data)))
        select_collection = set(select_data[i][0] for i in range(len(select_data)))
        same_collection = list(source_collection.intersection(select_collection))
        same_collection_count = len(same_collection)
        for collection in same_collection:
            current_count = same_collection.index(collection) + 1
            print(f'{current_count} of {same_collection_count} | {collection}')
            for tup_01 in source_data:
                if collection == tup_01[0]:
                    for tup_02 in select_data:
                        if tup_01[5] == tup_02[2]:
                            try:
                                collection_name = tup_01[0]
                                design_id = tup_01[1]
                                size = Common.find_size(tup_01[2])
                                source_price = tup_01[3]
                                select_price = tup_02[3]
                                brand = tup_01[4]
                                sku = tup_01[5]
                                upc = tup_01[6]
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
                                {'column': 'IsWarning', 'value': minus}
                            ]
                            db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[5], columns=columns)
        db.custom_query(db_file=db.db_file(), query=Common.sql_replace(table_name=db.db_table()[5])[0])
        db.custom_query(db_file=db.db_file(), query=Common.sql_replace(table_name=db.db_table()[5])[1])
        # db.custom_query(db_file=db.db_file(), query=Common.sql_replace(table_name=db.db_table()[5])[2])
        print('finish')
