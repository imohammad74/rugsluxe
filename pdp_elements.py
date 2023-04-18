import os

import requests

from common import Common
from table import PriceTable


class PDPElements:

    @staticmethod
    def page_is_exist(soup) -> bool:
        if soup.find(class_='OneColumn _404'):
            return False
        else:
            return True

    @staticmethod
    def is_in_stock(soup) -> bool:
        if soup.find(class_='pdp-title'):
            return True
        else:
            return False

    @staticmethod
    def brand(soup) -> str:
        """ get brand of product """
        brand = soup.find(class_='pdp-vendor')
        brand = Common.remove_quotes(brand)
        return brand

    @staticmethod
    def title(soup) -> str:
        """get title of pdp"""
        title = soup.find(class_='page-title').text
        title = title.replace(' ', '')
        title = Common.remove_quotes(title)
        return title

    @staticmethod
    def description(soup) -> str:
        desc = soup.find(class_='descTxt').text
        desc = Common.remove_quotes(desc)
        return desc

    @staticmethod
    def features_title(soup) -> list:
        content = soup.find_all(class_='rug-features-left')
        titles = [Common.remove_quotes(title.text) for title in content]
        return titles

    @staticmethod
    def feature_value(soup) -> list:
        content = soup.find_all(class_='rug-features-right')
        values = [Common.remove_quotes(value.text) for value in content]
        return values

    def features(self, soup) -> list:
        titles = self.features_title(soup)
        values = self.feature_value(soup)
        features = [{'title': titles[i], 'value': values[i]} for i in range(len(titles))]
        return features

    @staticmethod
    def images_product(url: str, soup: str, download_image: bool):
        images = soup.find_all('a', {'class': 'thumbnail'})
        main_url = 'https://www.rugstudio.com'
        image_links = [f'{main_url}{image.get("href")}' for image in images if '.aspx' not in image]
        cnt = 0
        sku = PriceTable.body(url, soup)[0]['Item #'].split('x')[0]
        path = f'{sku}'
        if download_image:
            for image in image_links:
                cnt += 1
                r = requests.get(image, allow_redirects=True, timeout=15)
                is_exist = os.path.exists(path)
                image_size = requests.head(image)
                image_format = image_size.headers.get('content-type').split('/')[-1]
                if not is_exist:
                    os.makedirs(path)
                if '.aspx' not in image:
                    file = open(f'{path}/{sku}-{cnt}.{image_format}', 'wb').write(r.content)
        else:
            return image_links

    @staticmethod
    def find_variant_url(soup: str, main_url: str) -> list:
        content = soup.find_all('a', {'data-slide-id': "slide-ac"})
        variant_url = list(set([f'{main_url}{url["href"]}' for url in content]))
        return variant_url

    def design_id(self, soup) -> str:
        title = self.title(soup).split('|')
        design_id = title[1].strip()
        return design_id

    @staticmethod
    def shape_size(soup) -> tuple:
        price_table = soup.find_all(class_='p-tile product_tile')
        variants = []
        for item in price_table:
            string = item.find(class_='sizedesc').text
            size = Common.find_size(string)
            shape = Common.find_shape(string)
            variant = (size, shape)
            variants.append(variant)
        return variants

    def collection(self, soup) -> str:
        """ get collection name"""
        title = self.title(soup).split('|')
        collection = title[0]
        collection = Common.remove_quotes(collection)
        collection = collection.strip()
        return collection
