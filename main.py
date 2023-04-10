import csv
import requests
from bs4 import BeautifulSoup
import sys
import os
import random



found_TF = False
try:
    path = sys._MEIPASS
except:
    path = os.path.abspath('.')

csv_path = os.path.join(path, "proxies.txt")
with open(csv_path, 'r') as f:
    lines = csv.reader(f)
    for line in lines:
        ips = line
rand_ip = random.choice(ips)
# print("IP: ", rand_ip)

HEADERS = ({'User-Agent':
                f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{rand_ip} Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

# Send a GET request to the Amazon product page for the given ASIN
url = f'https://www.amazon.com/dp/{asin}'
response = requests.get(url, headers=HEADERS)

# Create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, 'html.parser')
name = ''
price = ''
# Extract the product title and price from the page
name_element = soup.find('span', id='productTitle')
if name_element is not None:
    name = name_element.get_text().strip()
    found_TF = True

price_element = soup.find('span', attrs="a-offscreen")
if price_element is not None:
    price = price_element.get_text().strip()

# TODO:[] find the UPC too
upc = "N/A"

product_info = [found_TF, name, price, upc]

    return product_info