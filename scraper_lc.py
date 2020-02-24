import requests
from lxml import etree

def scrape_lc(book_id):
    url = 'https://www3.livrariacultura.com.br/' + book_id
    response = requests.get(url)
    print(response.content)

scrape_lc('bible-commentary-the-gospel-of-john-2012895340/p')