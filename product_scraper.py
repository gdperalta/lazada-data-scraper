"""Scrapes a list of sellers from Lazada by products.
Returns the following data in json format:
- Seller Name
- Seller ID (can be used in the future to fetch metrics and performance)
- Product Name
- Rating Score
- Review

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
    data = scrape_data()
    filter_data(data)
    # download_to_json()
    download_to_csv()


def scrape_data():
    response = requests.get(URL + query).text
    products_data = re.findall(r'"listItems":(.*),"breadcrumb"', response)
    str_products_data = ''.join(products_data)
    formatted_products_data = json.loads(str_products_data)

    return formatted_products_data


def filter_data(data):
    for d in data:
        filtered_data = {}
        for field in FIELD_NAMES:
            new_field = {field: unidecode(d.get(field, 'N/A'))}
            filtered_data.update(new_field)

        PRODUCTS_INFO.append(filtered_data)


def download_to_json():
    data = json.dumps(PRODUCTS_INFO, indent=4)
    with open('./data/product_search/product_lazada.json', 'w') as w:
        w.write(data)


def download_to_csv():
    with open('./data/product_search/product_lazada.csv', 'w',
              encoding='utf-8-sig', newline='') as w:
        data = csv.DictWriter(w, fieldnames=FIELD_NAMES)
        data.writeheader()
        data.writerows(PRODUCTS_INFO)


if __name__ == "__main__":
    main()
