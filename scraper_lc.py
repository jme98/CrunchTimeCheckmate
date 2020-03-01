import requests
from lxml import etree
from objects import *
from PIL import Image

def scrape_lc(book_id):
    url = 'https://www3.livrariacultura.com.br/' + book_id
    return requests.get(url)
    
def parse_lc(response, book_id):
    parsed = True

    root = etree.fromstring(response.content, etree.HTMLParser())
    data = SiteBookData()

    try:
        data.book_format = root.xpath("//td[@class='value-field Formato']")[0].text
    except:
        data.book_format = ""
        parsed = False

    try:
        data.book_image_url = root.xpath("//img[@id='image-main']/@src")[0]
        rspns = requests.get(data.book_image_url, stream=True)
        rspns.raw.decode_content = True
        data.book_image = Image.open(rspns.raw)
    except:
        data.book_image_url = ""
        data.book_image = ""

    try:
        data.isbn_13 = root.xpath("//td[@class='value-field ISBN']")[0].text
    except:
        data.isbn_13 = ""
        parsed = False

    try:
        data.description = root.xpath("//td[@class='value-field Sinopse']")[0].text
    except:
        data.description = ""
        parsed = False

    try:
        data.title = root.xpath("//h1[@class='title_product']/div")[0].text
    except:
        data.title = ""
        parsed = False

    try:
        data.subtitle = root.xpath("//span[@class='subtitle']")[0].text
    except:
        data.subtitle = ""

    data.authors = root.xpath("//td[@class='value-field Colaborador']/text()")
    if data.authors == []:
        parsed = False

    data.ready_for_sale = root.xpath("//button[@class='buy-in-page-button']") != []
    
    data.book_id = book_id
    data.site_slug = 'https://www3.livrariacultura.com.br/'
    data.url = data.site_slug + data.book_id
    data.content = response.content

    if (parsed):
        data.parse_status = "FULLY_PARSED"
    else:
        data.parse_status = "UNSUCCESSFUL"
    print(data.parse_status)

book_id = 'lord-of-the-rings-the-2639390/p'
response = scrape_lc(book_id)
sbd = parse_lc(response, book_id)
