import requests
from lxml import etree

def scrape_lc(bookid):
    url = 'https://www3.livrariacultura.com.br/' + bookid
    response = requests.get(url)
    return etree.fromstring(response.content, etree.HTMLParser())
    
def parse_lc(root):
    pass

root = scrape_lc('bible-commentary-the-gospel-of-john-2012895340/p')
sbd = parse_lc(root)