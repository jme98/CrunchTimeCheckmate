import requests
from lxml import etree

def scrapeLC(bookid):
    url = 'https://www3.livrariacultura.com.br/' + bookid
    response = requests.get(url)
    print(response.content)

scrapeLC('bible-commentary-the-gospel-of-john-2012895340/p')