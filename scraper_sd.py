import requests
from lxml import etree
from objects import *
from PIL import Image
class Scribd:
    #region fields
    slug = 'sd'
    base = 'https://www.scribd.com/'
    stripped = 'www.scribd.com' #url base, but stripped of surrounding 'https://' and '/'
    #endregion

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
        data.subtitle = _find_subtitle(root)
        data.authors = _find_authors(root)

        data.ready_for_sale = _find_ready_for_sale(root)
        data.book_id = url.strip('https://').strip(self.stripped).strip('/')
        data.site_slug = self.slug
        data.url = url
        data.content = response.content
        data.parse_status = _find_parse_status(data)

        return data

    def find_book_matches_at_site(self, book_data):
        pass

    def convert_book_id_to_url(self, book_id):
        return self.base + book_id

#region parse subfunctions
def _find_parse_status(data):
    if data.book_format != "" and data.isbn_13 != "" and data.description != "" and data.title != "" and data.authors != []:
        return "FULLY_PARSED"
    else:
        return "UNSUCCESSFUL"

def _find_book_format(root):
    try:
        book_format = root.xpath("//meta[@property='og:type']/@content")[0]
        if book_format != None:
            if book_format == 'book':
                return 'DIGITAL'
            else:
                return 'AUDIOBOOK'
        else:
            return ""
    except:
        return ""
    
def _find_book_image_url(root):
    try:
        book_image_url = root.xpath("//meta[@property='og:image']/@content")[0]
        if book_image_url != None:
            return book_image_url
        else:
            return ""
    except:
        return ""

def _find_book_image(url):
    try:
        rspns = requests.get(url, stream=True)
        rspns.raw.decode_content = True
        book_image = Image.open(rspns.raw)
        return book_image
    except:
        return None

def _find_isbn_13(root):
    try:
        isbn_13 = root.xpath("//meta[@property='books:isbn']/@content")[0]
        if isbn_13 != None:
            return isbn_13
        else:
            return ""
    except:
        return ""

def _find_description(root):
    try:
        description = root.xpath("//meta[@name='twitter:description']/@content")[0]
        if description != None:
            return description
        else:
            return ""
    except:
        return ""

def _find_title(root):
    try:
        title = root.xpath("//meta[@property='og:title']/@content")[0]
        if title != None:
            return title
        else:
            return ""
    except:
        return ""

def _find_subtitle(root):
    try:
        subtitle = root.xpath("//span[@class='subtitle']")[0].text
        if subtitle != None:
            return subtitle
        else:
            return ""
    except:
        return ""

def _find_authors(root):
    authors = root.xpath("//span[@class='author']/descendant::*/text()")
    if len(authors) > 1:
        return authors[1:]
    else:
        return []

def _find_ready_for_sale(root):
    return None
#endregion