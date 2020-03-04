import requests
from lxml import etree
from objects import *
from PIL import Image
class LivrariaCultura:
    #region fields
    slug = 'lc'
    base = 'https://www3.livrariacultura.com.br/'
    stripped = 'www3.livrariacultura.com.br' #url base, but stripped of surrounding 'https://' and '/'
    search = 'busca/'
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
        print(str(book_data))
        response = requests.get(self.base + self.search, params={"ft":str(book_data)})
        root = etree.fromstring(response.content, etree.HTMLParser())
        links = root.xpath("//div[@class='prateleiraProduto__informacao']//a/@href")
        results = []
        for l in links:
            results.append(self.get_book_data_from_site(l))
        for result in results:
            result = (result, self.evaluate_potential_match(book_data, result))

        return results

    def evaluate_potential_match(self, baseline, match):
        value = 0
        if baseline.isbn_13 == match.isbn_13:
            value += 1/2
        if baseline.title == match.title:
            value += 1/4
        if baseline.authors == match.authors:
            value += 1/8
        if baseline.book_format == match.book_format:
            value += 1/16
        if baseline.subtitle == match.subtitle:
            value += 1/32
        if baseline.series == match.series:
            value += 1/64
        if baseline.description == match.description:
            value += 1/128
        if baseline.book_image == match.book_image:
            value += 1/128
        return value

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
        book_format = root.xpath("//td[@class='value-field Formato']")[0].text
        if book_format != None:
            if book_format == 'LIVRO':
                return 'PRINT'
            elif book_format == 'ePub':
                return 'DIGITAL'
            else:
                return 'AUDIOBOOK'
        else:
            return ""
    except:
        return ""

def _find_book_image_url( root):
    try:
        book_image_url = root.xpath("//img[@id='image-main']/@src")[0]
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
        isbn_13 = root.xpath("//td[@class='value-field ISBN']")[0].text
        if isbn_13 != None:
            return isbn_13
        else:
            return ""
    except:
        return ""

def _find_description(root):
    try:
        description = root.xpath("//td[@class='value-field Sinopse']")[0].text
        if description != None:
            return description
        else:
            return ""
    except:
        return ""

def _find_title(root):
    try:
        title = root.xpath("//h1[@class='title_product']/div")[0].text
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
    return root.xpath("//td[@class='value-field Colaborador']/text()")

def _find_ready_for_sale(root):
    return root.xpath("//button[@class='buy-in-page-button']") != []
#endregion