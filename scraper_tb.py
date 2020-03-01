import requests
from lxml import etree

def scrape_tb(book_id):
    url = 'https://127.0.0.1:8000/TestBookstore/book_detail/' + book_id
    response = requests.get(url)
    return etree.fromstring(response.content, etree.HTMLParser())

def parse_tb(root):
    pass
