import requests
from lxml import etree
from objects import *

__MAIN_URL_TB__ = 'http://127.0.0.1:8000/TestBookStore/book_detail/'

def fetch_tb(book_id):
    url = __MAIN_URL_TB__ + book_id
    response = requests.get(url)
    return response

def parse_tb(content):
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    return root

def get_site_slug_from_url(url, book_id):
    pass #TODO: cut off book_id from the end & return the rest?

def is_available(etree_root):
    pass #TODO: release_date < today ? return True : return False

def get_isbn_13(etree_root):
    pass #TODO: get isbn, check if it's -10 or -13: if -10, convert to -13

def get_book_format(etree_root):
    pass #TODO: it will be DIGITAL, PRINT, or AUDIO

def get_series(etree_root):
    pass #TODO: this may return ""

def get_title(etree_root):
    pass #TODO

def get_subtitle(etree_root):
    pass #TODO: this may return ""

def get_authors(etree_root):
    pass #TODO: returns a list

def get_description(etree_root):
    pass #TODO

def get_extras_tb(etree_root):
    pass #TODO: returns a dict of the volume_no, price, release_date, & publisher

def no_undefined(book):
    pass #TODO: checks all SiteBookData fields EXCEPT series, subtitle, & extra; if any contains "None" then return false else return true

def create_sitebookdata_tb(book_id):
    book = SiteBookData()

    html_data = fetch_tb(book_id)
    root = parse_tb(html_data.content)
    
    #get some of the SiteBookData attributes through clever code
    book.page_content = html_data.content
    book.url = html_data.url
    book.book_id = book_id
    book.site_slug = get_site_slug_from_url(book.url, book.book_id)

    #get the other SiteBookData attributes through xpath
    book.ready_for_sale = is_available(root)
    book.isbn_13 = get_isbn_13(root)
    book.book_format = get_book_format(root)

    book.series = get_series(root)
    book.title = get_title(root)
    book.subtitle = get_subtitle(root)
    book.authors = get_authors(root)
    book.description = get_description(root)

    book.extra = get_extras_tb(root)

    if no_undefined(book):
        book.parse_status = "FULLY_PARSED"
    else:
        book.parse_status = "UNSUCCESSFUL"

    return book