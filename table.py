import time

from common import Common


class PriceTable:

    @staticmethod
    def main(params) -> list:
        category = params['category']
        soup = params['data']
        if category == 'pillow':
            time.sleep(2)
            price_table = soup.find_all(class_='swatch-attribute-options clearfix toggle_body')[1]
            time.sleep(1)
            products = price_table.find_all(class_='price')
            variants = []
            for variant in products:
                size = variant.find(class_='label').text
                price = variant.find(class_='price').text
                variant_ = {
                    'price': Common.clean_price(price),
                    'size': Common.find_size(size),
                }
                print(variant_)
                variants.append(variant_)
            return variants
        if category == 'rug':
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
                print(variants)
            return variants


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
