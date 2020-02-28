import requests
from lxml import etree
from objects import *

def scrape_lc(book_id):
    url = 'https://www3.livrariacultura.com.br/' + book_id
    return requests.get(url)
    
def parse_lc(response, book_id):
    root = etree.fromstring(response.content, etree.HTMLParser())
    data = SiteBookData()

    data.book_format = root.xpath("//td[@class='value-field Formato']")[0].text
    data.book_image = root.xpath("//img[@id='image-main']/@src") #
    data.book_image_url = root.xpath("//img[@id='image-main']/@src")
    data.isbn_13 = root.xpath("//td[@class='value-field ISBN']")[0].text #
    try:
        data.description = root.xpath("//td[@class='value-field Sinopse']")[0].text
    except:
        data.description = ""
    data.title = root.xpath("//h1[@class='title_product']/div")[0].text
    data.subtitle = root.xpath("//span[@class='subtitle']")[0].text
    data.authors = root.xpath("//td[@class='value-field Colaborador']/text()")
    data.book_id = book_id
    data.site_slug = 'https://www3.livrariacultura.com.br/'
    data.url = data.site_slug + data.book_id
    data.content = response.content
    print(data.url)

book_id = 'lord-of-the-rings-the-2639390/p'
response = scrape_lc(book_id)
sbd = parse_lc(response, book_id)
