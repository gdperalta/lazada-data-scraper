"""Scrapes a list of sellers from Lazada by products.
Returns the following data in json format:
- Name (of product)
- Image
- Original Price
- Price
- Discount
- Rating Score
- Review
- Location
- Brand ID
- Brand Name
- Seller ID (can be used in the future to fetch metrics and performance)
- Seller Name
- Item URL

Author: Godfrey Peralta <godfrey@kayafounders.com>

Created: July 4, 2022
"""

import requests  # handles communication with api
import re        # handles regex matches
import json      # handles conversion to json
import csv       # handles conversion to csv

from unidecode import unidecode  # represents unicode text in ASCII


URL = 'https://www.lazada.com.ph/catalog/?from=input&q='
query = 'laptop&location=Local&rating=4'
FIELD_NAMES = [
                'name',
                'image',
                'originalPrice',
                'price',
                'discount',
                'ratingScore',
                'review',
                'location',
                'brandId',
                'brandName',
                'sellerId',
                'sellerName',
                'itemUrl'
              ]
PRODUCTS_INFO = []


def main():
    products_data = scrape_data()
    iterate_data(products_data)
    # download_to_json()
    download_to_csv()


def scrape_data():
    response = requests.get(URL + query).text
    products_data = re.findall(r'"listItems":(.*),"breadcrumb"', response)
    str_products_data = ''.join(products_data)
    formatted_products_data = json.loads(str_products_data)

    return formatted_products_data


def iterate_data(data):
    for products in data:
        filtered_data = filter_data(products)

        PRODUCTS_INFO.append(filtered_data)   


def filter_data(data):
    filtered_data = {}
    for field in FIELD_NAMES:
        value = unidecode(data.get(field, 'N/A'))

        # for evaluation of better solution
        if field == 'itemUrl':
            value = value.replace('//', '', 1)

        new_field = {field: value}
        filtered_data.update(new_field)

    return filtered_data


def download_to_json():
    data = json.dumps(PRODUCTS_INFO, indent=4)
    with open('./data/product_search/product_lazada.json', 'w') as file:
        file.write(data)


def download_to_csv():
    with open('./data/product_search/product_lazada.csv', 'w',
              encoding='utf-8-sig', newline='') as file:
        data = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        data.writeheader()
        data.writerows(PRODUCTS_INFO)


if __name__ == "__main__":
    main()
