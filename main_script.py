import requests
from bs4 import BeautifulSoup

from check_price import CheckPrice
from common import Common
from db import DBManagement as db
from get_brands_url import GetBrandsURL
from mail import Mail
from pdp import PDP


class Main:
    print('Welcome to RugsDirect Crawler')

    @staticmethod
    def find_last_crawled_url():
        last_url = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[4], all_columns=False,
                                  columns=['seq'], condition="name='URLs'")
        last_url = int(last_url[0][0])
        return last_url

    @staticmethod
    def params(url: str) -> dict:
        re = requests.get(url)
        soup = BeautifulSoup(re.content, "html.parser")
        params = {
            'url': url,
            're': re,
            'soup': soup
        }
        return params

    @staticmethod
    def get_urls(all_brand: bool, pillows: bool):
        categories = [
            {'category_name': 'rug', 'url': "https://rugsluxe.com/area-rugs.html"},
            {'category_name': 'pillow', 'url': 'https://rugsluxe.com/pillows.html'}
        ]
        if all_brand and pillows is True:
            for category in categories:
                category_name = category['category_name']
                GetBrandsURL(category_name=category_name)
        elif pillows is True:
            category_name = categories[1]['category_name']
            GetBrandsURL(category_name=category_name)
        else:
            category_name = categories[0]['category_name']
            GetBrandsURL(category_name=category_name)

    def get_pdp(self, resume: bool, category_name: str):
        # max_worker = Common.max_worker()
        urls = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[0], all_columns=False,
                              columns=['url_address', 'brand', 'category'])
        total_urls = len(urls)
        last_url_id = self.find_last_crawled_url()
        if resume:
            print(last_url_id)
            print(total_urls)
            params = {
                'category': category_name,
                'data': urls,
                'total_urls': total_urls,
                'start_point': last_url_id
            }
            PDP(params)

        else:
            all_urls = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[0], all_columns=False,
                                      columns=['url_address', 'brand', 'category'])
            pillow_urls = [(url[0], url[1], url[2]) for url in all_urls if url[2] == 'pillow']
            rug_urls = [(url[0], url[1], url[2]) for url in all_urls if url[2] == 'rug']
            params = {
                'category': category_name,
                'data': rug_urls if category_name == 'rug' else pillow_urls,
                'total_urls': len(rug_urls) if category_name == 'rug' else len(pillow_urls),
                'start_point': 0
            }
            PDP(params)
        db.custom_query(db_file=db.db_file(), query=Common.sql_replace(table_name=db.db_table()[2])[0])
        db.custom_query(db_file=db.db_file(), query=Common.sql_replace(table_name=db.db_table()[2])[1])

    def __init__(self):
        while True:
            print('''
                [1]: Get All URLs
                [2]: Get Some Rugs Brand URLs
                [3]: Get Rugs PDP
                [4]: Resume Get PDPs
                [5]: Check Price
                [6]: Get Pillows URLs
                [7]: Get Pillows PDP
                ''')
            select_option = input("Enter a option: ")
            if select_option == '1':
                self.get_urls(all_brand=True, pillows=True)
            elif select_option == '2':
                self.get_urls(all_brand=False, pillows=False)
            elif select_option == '3':
                # Mail(attachment=False)
                self.get_pdp(resume=False, category_name='rug')
            elif select_option == '4':
                # Mail(attachment=False)
                self.get_pdp(resume=True, category_name='rug')
            elif select_option == '5':
                Mail(attachment=True)
                CheckPrice()
            elif select_option == '6':
                # Mail(attachment=False)
                self.get_urls(all_brand=False, pillows=True)
            elif select_option == '7':
                # Mail(attachment=False)
                self.get_pdp(resume=False, category_name='pillow')
            else:
                continue


Main()
