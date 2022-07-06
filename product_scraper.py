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
import csv

URL = 'https://www.lazada.com.ph/catalog/?from=input&q='
FIELD_NAMES = [
                'product_name',
                'image',
                'original_price',
                'price',
                'discount',
                'rating_score',
                'reviews',
                'location',
                'brand_id',
                'brand_name',
                'seller_id',
                'seller_name',
                'item_url'
              ]
query = 'laptop&location=Local&rating=4'
PRODUCTS_INFO = []
# search = input('Search item in Lazada: ')


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
        filtered_data = {
            "product_name": d['name'],
            "image": d['image'],
            "original_price": d.get('originalPrice', ''),
            "price": d['price'],
            "discount": d.get('discount', 'N/A'),
            "rating_score": d['ratingScore'],
            "reviews": d['review'],
            "location": d['location'],
            "brand_id": d['brandId'],
            "brand_name": d['brandName'],
            "seller_id": d['sellerId'],
            "seller_name": d['sellerName'],
            "item_url": d['itemUrl'],
        }

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
