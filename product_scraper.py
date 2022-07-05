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

URL = 'https://www.lazada.com.ph/catalog/?from=input&q='
query = 'laptop&location=Local&rating=4'
PRODUCTS_INFO = []
# search = input('Search item in Lazada: ')


def main():
    data = scrape_data()
    filter_data(data)
    download_data()


def scrape_data():
    response = requests.get(URL + query).text
    products_data = re.findall(r'"listItems":(.*),"breadcrumb"', response)
    str_products_data = ''.join(products_data)
    formatted_products_data = json.loads(str_products_data)

    return formatted_products_data


def filter_data(data):
    for d in data:
        filtered_data = {
            "SellerName": d['sellerName'],
            "SellerId": d['sellerId'],
            "ProductName": d['name'],
            "RatingScore": d['ratingScore'],
            "Review": d['review'],
        }

        PRODUCTS_INFO.append(filtered_data)


def download_data():
    data = json.dumps(PRODUCTS_INFO, indent=4)
    with open('./data/product_search/product_lazada.json', 'w') as w:
        w.write(data)


if __name__ == "__main__":
    main()
