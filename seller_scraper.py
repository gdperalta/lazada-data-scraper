import requests
import re

url = 'https://www.lazada.com.ph/shop'
query = '/watsons?path=profile.htm'
# search = input('Search item in Lazada: ')

txt = requests.get(url + query).text
# txt.replace("\","")
with open('./data/seller_profile/seller_lazada.txt','w') as w:
    script = re.findall(r'window.__translations__ =(.*)', txt)
    str_scr = ''.join(script)
    print(str_scr, file=w)