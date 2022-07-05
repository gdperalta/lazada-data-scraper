import requests
import re
import json

url = 'https://www.lazada.com.ph/catalog/?from=input&q='
query = 'laptop&location=Local&rating=4'
# search = input('Search item in Lazada: ')

txt = requests.get(url + query).text
script = re.findall(r'"listItems":(.*),"breadcrumb"', txt)
str_scr = ''.join(script)
products_data = json.loads(str_scr)
filtered_data = []

for product in products_data:
    s = {
            "Name": product['name'],
            "RatingScore": product['ratingScore'],
            "Review": product['review'],
            "SellerId": product['sellerId'],
            "SellerName": product['sellerName'],
        }
    filtered_data.append(s)

json_data = json.dumps(filtered_data, indent = 4)

with open('./data/product_search/product_lazada.json','w') as w:
    w.write(json_data)
