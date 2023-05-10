# import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from common import Common
from db import DBManagement as db

now = datetime.now()


class GetAllBrandsURL:

    @staticmethod
    def main(params):
        """This function is main function in this script and get urls and insert them to database."""
        category = params['category']
        brand = params['brand']
        main_url = params['url']
        url_list = Common.last_url(params['soup'])
        for url in url_list:
            if url == 0:
                plp_url = main_url
            else:
                plp_url = f"{main_url}&p={url}"
            r = requests.get(plp_url)
            soup = BeautifulSoup(r.content, "html.parser")
            a_tags = soup.find_all(class_='product-item-link')
            for pdp_url in a_tags:
                current_time = int(now.strftime("%y%m%d"))
                url = pdp_url['href']
                db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[0], log=False, columns=[
                    {
                        'column': 'url_address',
                        'value': url,
                    },
                    {
                        'column': 'last_update',
                        'value': current_time,
                    },
                    {
                        'column': 'brand',
                        'value': brand,
                    },
                    {
                        'column': 'category',
                        'value': category,
                    }
                ])
        print(f'{category} -> {brand} finish!')

    def __init__(self, params):
        self.main(params)
