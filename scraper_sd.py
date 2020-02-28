import requests
from lxml import etree

def scrape_lc(book_id):
    url = 'https://www.scribd.com/' + book_id
    response = requests.get(url)
    return etree.fromstring(response.content, etree.HTMLParser())
    
def parse_lc(root):
    pass

root = scrape_lc('book/295105408/The-MacArthur-Study-Bible')
sbd = parse_lc(root)
