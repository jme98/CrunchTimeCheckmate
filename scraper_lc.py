import requests
from lxml import etree

<<<<<<< HEAD
def scrape_lc(bookid):
    url = 'https://www3.livrariacultura.com.br/' + bookid
    response = requests.get(url)
    return etree.fromstring(response.content, etree.HTMLParser())
    
def parse_lc(root):
    pass

root = scrape_lc('bible-commentary-the-gospel-of-john-2012895340/p')
sbd = parse_lc(root)
=======
def scrape_lc(book_id):
    url = 'https://www3.livrariacultura.com.br/' + book_id
    response = requests.get(url)
    print(response.content)

scrape_lc('bible-commentary-the-gospel-of-john-2012895340/p')
>>>>>>> master
