from common import Common


class PriceTable:

    @staticmethod
    def main(soup) -> list:
        # driver.get(url)
        #  time.sleep(0.5)
        # html = driver.page_source
        # soup = BeautifulSoup(html, 'html.parser')

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
