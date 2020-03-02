import io
import requests
from lxml import etree
from objects import *
from PIL import Image

def scrape_gb(book_id):
    url = 'https://books.google.com/books?id=' + book_id
    response = requests.get(url)
    return response.content

def parse(book_id, response):
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(response), parser)
    root = tree.getroot()
    data = SiteBookData()

    data.book_id = book_id
    data.site_slug = 'https://books.google.com/books?id='
    data.title = root.xpath(".//meta[@name='title']")[0].get("content")
    data.description = root.xpath(".//meta[@name='description']")[0].get("content")
    data.url = data.site_slug + data.book_id
    data.book_image_url = root.xpath(".//link[@rel='image_src']")[0].get("href")
    stuff = root.xpath(".//span[@dir='ltr']")
    p = root.xpath(".//a[@id='gb-get-book-content']")[0].text
    print(p)
    
    
    count = 0
    author_start = 0
    isbn_start = 0
    sub_done = 0
    series_start = 0
    for i in stuff:
        #print(str(count) + ": " + i.text)
        if ("Author" in i.text):
            author_start = count + 1
            series_start = count - 1
        if ("ISBN" in i.text):
            isbn_start = count + 1
        if data.title in i.text and sub_done == 0:
            data.subtitle = stuff[count + 1].text
            sub_done = 1
        if "Book" in i.text[0:4] and i.text[5].isdigit():
            data.series = i.text
        count = count + 1
    
    while "Edition" not in stuff[author_start].text and "Publisher" not in stuff[author_start].text and "Illustrated by" not in stuff[author_start].text:
        data.authors.append(stuff[author_start].text)
        author_start = author_start + 1

    isbn_str = ""
    ready = 0
    for i in stuff[isbn_start].text:
        if i is " ":
            ready = 1
        elif ready == 1:
            isbn_str = isbn_str + i

    for i in data.authors:
        if i in data.subtitle:
            data.subtitle = ""
    data.isbn_13 = isbn_str
    data.content = response
    data.ready_for_sale = None
    data.book_format = None
    data.parse_status = "FULLY_PARSED"

    try:
        r = requests.get(data.book_image_url, stream = True)
        r.raw.decode_content = True
        data.book_image = Image.open(r.raw)
    except:
        data.book_image = None

id = "LhTuQAAACAAJ" #artemis fowl and the time paradox - series
id = "dWALVMNK5kkC" #click - multiple authors
id = "orb2rQEACAAJ" #tess a pure woman - subtitle
id = "kTH6zAEACAAJ" #hp and the philosopher's stone - series
id = "PocJx9t4wbUC" #ranger's apprentice - series
id = "ykZK_50nUOAC" #mercy blade - price

res = scrape_gb(id)

data = parse(id, res)