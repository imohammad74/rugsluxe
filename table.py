import json


class PriceTable:

    @staticmethod
    def find_product(soup: str) -> dict:
        txt = str(soup)
        find_product = txt.split('"offers": [')
        find_product = find_product[1].split(']')
        products = find_product[0]
        products_string = '[' + products + ']'
        products_json = json.loads(products_string)
        return products_json

    def main(self, params) -> list:
        category = params['category']
        soup = params['data']
        if category == 'pillow':
            variants = self.find_product(soup)
            products = []
            for variant in variants:
                sku = variant['sku']
                price = variant['price']
                variant_ = {
                    'price': price,
                    'sku': sku,
                }
                products.append(variant_)
                return products
        if category == 'rug':
            variants = self.find_product(soup)
            products = []
            for variant in variants:
                sku = variant['sku']
                price = variant['price']
                variant_ = {
                    'price': price,
                    'sku': sku,
                }
                products.append(variant_)
        return products

    def __init__(self, soup):
        self.main(soup)


'''
        price_table = soup.find(class_='swatch-attribute size')
        in_stock_products = price_table.find_all(class_='swatch-select-2 selectClass2Custom2')
        out_stock_products = price_table.find_all(class_='swatch-select-2 selectClass2Custom2 disabled')
        products = in_stock_products + out_stock_products
        variants = []
        for variant in products:
            size = variant.find(class_='label').text
            shape = variant.find(class_='shape').text
            price = variant.find(class_='price2').text
            variant_ = {
                'price': Common.clean_price(price),
                'size': Common.find_size(size),
                'shape': Common.find_shape(shape),
            }
            variants.append(variant_)
        return variants
'''
