import io
import requests
from lxml import etree
from objects import *
from PIL import Image


class GoogleBooks:
    slug = 'gb'
    base = 'https://books.google.com/'
    stripped = 'books.google.com'

    def get_book_data_from_site(self, url):
        response = requests.get(url)
        root = etree.fromstring(response.content, etree.HTMLParser())
        data = SiteBookData()

        data.book_format = _find_book_format(root)
        data.book_image_url = _find_book_image_url(root)
        data.book_image = _find_book_image(data.book_image_url)
        data.isbn_13 = _find_isbn_13(root)
        data.description = _find_description(root)
        data.title = _find_title(root)
        data.authors = _find_authors(root)
        data.subtitle = _find_subtitle(root, data.title, data.authors)

        data.ready_for_sale = _find_ready_for_sale(root)
        data.book_id = "books?id=" + url.strip('https://').strip(self.stripped).strip('/')
        data.site_slug = self.slug
        data.url = url
        data.content = response.content
        data.series = _find_series(root)
        data.parse_status = _find_parse_status(data)
        print(data)

        return data

    def find_book_matches_at_site(self, book_data):
        pass

    def convert_book_id_to_url(self, book_id):
        return self.base + book_id

    def construct_params_of_search(book_data):


def _find_book_format(root):
    try:
        p = root.xpath(".//a[@id='gb-get-book-content']")[0].text
        if "buy" in p.lower() and "ebook" in p.lower():
            return "DIGITAL"
        elif "get print" in p.lower():
            return "PRINT"
        else:
            return ""
    except:
        return ""

def _find_book_image_url(root):
    try:
        biu = root.xpath(".//link[@rel='image_src']")[0].get("href")
        if biu != None:
            return biu
        else:
            return "" 
    except:
        return ""

def _find_book_image(biu):
    try:
        r = requests.get(biu, stream = True)
        r.raw.decode_content = True
        bi = Image.open(r.raw)
        return bi
    except:
        return None

def _find_isbn_13(root):
    try:
        stuff = root.xpath(".//span[@dir='ltr']")
        count = 0
        isbn_start = 0
        for i in stuff:
            if ("ISBN" in i.text):
                isbn_start = count + 1
            count = count + 1
        isbn_str = ""
        ready = 0
        for i in stuff[isbn_start].text:
            if i is " ":
                ready = 1
            elif ready == 1:
                isbn_str = isbn_str + i

        return isbn_str
    except:
        return ""

def _find_description(root):
    try:
        desc = root.xpath(".//meta[@name='description']")[0].get("content")
        if desc != None:
            return desc
        else:
            return ""
    except:
        return ""

def _find_title(root):
    try:
        t = root.xpath(".//meta[@name='title']")[0].get("content")
        if t != None:
            return t
        else:
            return ""
    except:
        return ""

def _find_subtitle(root, title, authors):
    try:
        stuff = root.xpath(".//span[@dir='ltr']")
        count = 0
        sub_done = 0
        sub = ""
        for i in stuff:
            if title in i.text and sub_done == 0:
                sub = stuff[count + 1].text
                sub_done = 1
            count = count + 1
        for i in authors:
            if i in data.subtitle:
                s = ""
        if sub != None:
            return sub
        else:
            return ""
    except:
        return ""

def _find_authors(root):
    try:
        stuff = root.xpath(".//span[@dir='ltr']")
        count = 0
        author_start = 0
        aList = []
        for i in stuff:
            if ("Author" in i.text):
                author_start = count + 1
            count = count + 1
        
        while "Edition" not in stuff[author_start].text and "Publisher" not in stuff[author_start].text and "Illustrated by" not in stuff[author_start].text:
            aList.append(stuff[author_start].text)
            author_start = author_start + 1
        return aList
    except:
        return []
    
def _find_ready_for_sale(root):
    try:
        p = root.xpath(".//a[@id='gb-get-book-content']")[0].text
        rfs = False
        if "buy" in p.lower() or "get print" in p.lower():
            data.ready_for_sale = True
        return rfs
    except:
        return None

def _find_parse_status(data):
    if data.book_format != "" and data.isbn_13 != "" and data.description != "" and data.title != "" and data.authors != []:
        return "FULLY_PARSED"
    else:
        return "UNSUCCESSFUL"

def _find_series(root):
    try:
        stuff = root.xpath(".//span[@dir='ltr']")
        s = ""
        count = 0
        for i in stuff:
            if "book" in i.text[0:4].lower() and i.text[5].isdigit():
                s = i.text
            count = count + 1
        if s != None:
            return s
        else:
            return ""
    except:
        return ""