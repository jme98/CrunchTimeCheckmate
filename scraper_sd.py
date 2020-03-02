import requests
from lxml import etree
from objects import *
from PIL import Image

def scrape_lc(book_id):
    url = 'https://www.scribd.com/' + book_id
    open('sdsample.txt', 'wb').write(requests.get(url).content)
    return requests.get(url)
    
def parse_lc(response, book_id):
    parsed = True

    root = etree.fromstring(response.content, etree.HTMLParser())
    data = SiteBookData()

    try:
        data.book_format = root.xpath("//meta[@property='og:type']/@content")[0]
    except:
        data.book_format = ""
        parsed = False

    try:
        data.book_image_url = root.xpath("//meta[@property='og:image']/@content")[0]
        rspns = requests.get(data.book_image_url, stream=True)
        rspns.raw.decode_content = True
        data.book_image = Image.open(rspns.raw)
    except:
        data.book_image_url = ""
        data.book_image = ""

    try:
        data.isbn_13 = root.xpath("//meta[@property='books:isbn']/@content")[0]
    except:
        data.isbn_13 = ""
        parsed = False

    try:
        data.description = root.xpath("//meta[@name='twitter:description']/@content")[0]
    except:
        data.description = ""
        parsed = False

    try:
        data.title = root.xpath("//meta[@property='og:title']/@content")[0]
    except:
        data.title = ""
        parsed = False

    data.authors = root.xpath("//span[@class='author']/descendant::*/text()")
    try:
        data.authors = data.authors[1:]
    except:
        parsed = False

    data.ready_for_sale = False
    
    data.book_id = book_id
    data.site_slug = 'https://www.scribd.com/'
    data.url = data.site_slug + data.book_id
    data.content = response.content

    if (parsed):
        data.parse_status = "FULLY_PARSED"
    else:
        data.parse_status = "UNSUCCESSFUL"
    data.book_image.show()

book_id = 'book/295105408/The-MacArthur-Study-Bible'
root = scrape_lc(book_id)
sbd = parse_lc(root, book_id)
