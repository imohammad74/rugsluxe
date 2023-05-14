import re

from db import DBManagement as db


class Common:

    @staticmethod
    def last_url(soup) -> list:
        """
        this function helps to get end of urls.
        for ex: https://rugsluxe.com/area-rugs.html?p=2&product_list_limit=96 ; 2 is returned by this function.
        """
        last_url_string = soup.find(class_='page-of').text
        last_url = int(re.search(r'\d+', last_url_string).group())
        urls = [i + 1 for i in range(0, last_url)]
        return urls

    @staticmethod
    def get_url(plp_url):
        main_url = 'https://www.rugs-direct.com'
        url = f"{main_url}{plp_url['href']}"
        return url

    @staticmethod
    def convert_sup_sub_to_str(size):
        r = size.replace('<sup>', '')
        r = r.replace('<sub>', '')
        r = r.replace('</sup>', '')
        size = r.replace('</sub>', '').strip()
        return size

    @staticmethod
    def clean_price(price):
        if '$' in price:
            price = price.replace('$', '')
        if ',' in price:
            price = price.replace(',', '')
        return price

    @staticmethod
    def brand_from_url(url):
        title = url.replace('https://www.rugstudio.com/', '')
        brand = title.split('-')[0]
        return brand

    @staticmethod
    def design_id_pattern_i(title):
        """
        Rugs have some patterns from designID. In Rugstudio, there are two patterns. In this pattern, designID has the
        digital number in its pattern.
        """
        title_separate = title.split(" ")
        for character in title_separate:
            if re.findall('[0-9]', character):
                design_id = character
                return design_id

    @staticmethod
    def design_id_pattern_ii(title: str, brand: str, collection_name: str):
        """
        Rugs have some patterns from designID. In Rugstudio, there are two patterns. In this pattern, designID is a
        word. The location of this word is different in the brands title.
        """
        title_ = title.lower().split(' ')
        print(f'title: {title_}')
        brand_ = brand.lower().split(' ')
        print(f'brand_: {brand_}')
        collection_name_ = collection_name.lower().split(' ')
        print(f'collection_name_: {collection_name_}')
        title_collection = brand_ + collection_name_
        print(f'title_collection: {title_collection}')
        design_id = []
        for part in title_:
            if part in title_collection:
                continue
            else:
                design_id.append(part)
        if len(design_id) == 1:
            design_id = design_id[:-3][0]
            return design_id
        else:
            design_id = f'{design_id[:-3][0]} {design_id[:-3][1]}'
            return design_id

    @staticmethod
    def max_worker():
        """
        Fetch max worker from database
        """
        max_worker = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[4], all_columns=False,
                                    columns=['seq'], condition="name='max_worker'")
        max_worker = int(max_worker[0][0])
        return max_worker

    @staticmethod
    def find_shape(size_string: str):
        string_ = size_string.split(' ')
        pattern = re.compile(r'^[a-zA-Z]+$')
        shape = []
        for item in string_:
            if len(item) > 1 and pattern.match(item):
                item = item.capitalize()
                shape.append(item)
        shape = 'Runner' if 'Runner' in shape else shape[0]
        return shape

    @staticmethod
    def find_size(size_string: str) -> str:
        string_ = size_string.split(' ')
        pattern = re.compile(r'^[a-wyzA-WYZ]+$')
        size = []
        for item in string_:
            if not pattern.match(item):
                size.append(item)
        seperator = ' '
        size = seperator.join(size)
        size = size.replace(" ", "")
        size = size.replace("'", "-")
        size = size.replace('"', "+")
        return size

    @staticmethod
    def remove_quotes(string: str) -> str:
        """
        Removes single quotes and double quotes from a string.
        """
        clean_string = string.replace("'", "").replace('"', '')
        return clean_string

    @staticmethod
    def sql_replace(table_name) -> tuple:
        """
        after complete insert data to database, run it and current the size column.
        :return: replace string in a tuple
        """
        to_double_quote = f"""UPDATE {table_name} SET size = REPLACE(size, '+', '"')"""
        to_single_quote = f"""UPDATE {table_name} SET size = REPLACE(size, '-', "'")"""
        to_small_case = f"""UPDATE {table_name} SET size = REPLACE(size, 'X', "x")"""
        return to_single_quote, to_double_quote, to_small_case
