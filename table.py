from common import Common


class PriceTable:

    @staticmethod
    def main(soup):
        price_table = soup.find_all(class_='p-tile product_tile')
        variants = []
        for variant in price_table:
            variant_ = {
                'msrp': Common.clean_price(variant['data-msrp']),
                'price': Common.clean_price(variant['data-price']),
                'product_name': variant.find(class_='sizedesc').text
            }
            variants.append(variant_)
        return variants
