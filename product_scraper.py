import requests
import re


url = 'https://www.lazada.com.ph/catalog/?from=input&q='
query = 'laptop&location=Local&rating=4'
# search = input('Search item in Lazada: ')

txt = requests.get(url + query).text
# txt.replace("\","")
with open('./data/product_search/product_lazada.txt','w') as w:
    script = re.findall(r'"listItems":(.*)', txt)
    str_scr = ''.join(script)
    print(str_scr, file=w)