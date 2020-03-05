import requests, io
from lxml import etree
from objects import *
from datetime import datetime

__MAIN_URL_TB__ = "http://127.0.0.1:8000/TestBookStore/book_detail/"

def fetch_tb(book_id):
    url = __MAIN_URL_TB__ + book_id
    response = requests.get(url)
    return response

def parse_tb(content):
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    return root

def get_site_slug_from_url(url):
    if "http://127.0.0.1:8000/TestBookStore/book_detail/" in url:
        return "tb"
    return None

def parse_date_string(date_string):
    truncate_index = date_string.rfind(",") #locate the comma that comes after the year
    fixed_string = date_string[1:truncate_index] #remove the offending comma and everything after it, as well as the leading whitespace
    date_object = datetime.strptime(fixed_string, "%b. %d, %Y") #convert to a datetime object via careful formatting
    return date_object

def get_release_date(etree_root):
    xpath = "//p/strong[normalize-space(text()) = 'Release Date:']/following-sibling::text()"
    date_string = etree_root.xpath(xpath)[0]
    release_date = parse_date_string(date_string)
    return release_date

def is_available(etree_root):
    release_date = get_release_date(etree_root)
    now_date = datetime.now()
    if release_date.date() < now_date.date():
        return True
    return False

def calc_check_digit(isbn_string):
    products = []
    for i in range(0, 12):
        if ((i + 1) % 2) != 0: #we are looking at the first, third, fifth ... digit
            products[i] = isbn_string[i] * 1
        else: #we are looking at the second, fourth, sixth ... digit
            products[i] = isbn_string[i] * 3

    accumulator = 0
    for p in products:
        accumulator += p

    modulated = accumulator % 10

    if modulated == 0:
        check_digit = modulated
    else:
        check_digit = 10 - modulated

    return check_digit
    
def format_isbn(isbn_string):
    if len(isbn_string) == 13:
        return isbn_string
    elif len(isbn_string) == 10:
        nine_digits = isbn_string[0:9] #slice off the old check digit
        final_isbn = "978"
        final_isbn.append(nine_digits)
        final_isbn.append(calc_check_digit(final_isbn))
        return final_isbn
    else:
        return None

def get_isbn_13(etree_root):
    xpath = "//p/strong[normalize-space(text()) = 'ISBN 13:']/following-sibling::text()"
    isbn_string = etree_root.xpath(xpath)[0]
    isbn_string = isbn_string[1:] #remove the leading whitespace
    isbn_13_string = format_isbn(isbn_string)
    return isbn_13_string

def get_book_format(etree_root):
    xpath = "//p/strong[normalize-space(text()) = 'ISBN 13:']/following-sibling::text()"
    format_code = etree_root.xpath(xpath)[0]
    format_code = format_code[1:] #remove the leading whitespace
    if format_code[0] == "E":
        return "DIGITAL"
    elif format_code[0] == "A" and format_code not in ["A205", "A206", "A211", "A212"]:
        return "AUDIO"
    elif format_code[0] == "B":
        return "PRINT"
    else:
        return None

def get_series(etree_root):
    xpath = "//p/strong[normalize-space(text()) = 'Series Name:']/following-sibling::text()"
    series_name = etree_root.xpath(xpath)[0]
    series_name = series_name[1:] #remove leading whitespace
    if series_name == "N/A":
        return ""
    else:
        return series_name

def get_title(etree_root): 
    xpath = "//body/h1"
    title_line = etree_root.xpath(xpath)[0]
    title = title_line[12:]
    return title

def get_subtitle(etree_root):
    xpath = "//p/strong[normalize-space(text()) = 'Subtitle:']/following-sibling::text()"
    subtitle = etree_root.xpath(xpath)[0]
    subtitle = subtitle[1:] #remove leading whitespace
    if subtitle == "N/A":
        return ""
    else:
        return subtitle

def get_authors(etree_root):
    xpath = "//body/ul/p"
    authors = etree_root.xpath(xpath)

    authors_list = []
    for a in authors:
        full_name = a.text
        given_name = a.split()[0]
        surname = a.split()[1]
        authors_list.append({given_name, surname})

    return authors_list

def get_description(etree_root):
    pass #TODO: xpath won't get the last <p> tag in the page correctly, so use string searching to find it

def get_volume_no(etree_root):
    xpath = "//p/strong[normalize-space(text()) = 'Volume Number:']/following-sibling::text()"
    volume_no = etree_root.xpath(xpath)[0]
    volume_no = volume_no[1:] #remove leading whitespace
    if volume_no == "N/A":
        return ""
    else:
        return volume_no

def get_price(etree_root):
    xpath = "//p/strong[normalize-space(text()) = 'Price:']/following-sibling::text()"
    price = etree_root.xpath(xpath)[0]
    price = price[1:] #remove leading whitespace
    final_string = "$"
    final_string.append(price)
    return final_string

def get_extras_tb(etree_root):
    extras = {}
    extras["volume_no"] = get_volume_no(etree_root)
    extras["price"] = get_price(etree_root)
    extras["release_date"] = get_release_date(etree_root)
    return extras

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
    book.site_slug = get_site_slug_from_url(book.url)

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

if __name__ == "__main__":
    #THIS IS TEST CODE
    content = fetch_tb("781524243456").content
    print(content)
    root = parse_tb(content)
    #CALL AND DEBUG EACH METHOD INDIVIDUALLY, STARTING WITH get_description()
