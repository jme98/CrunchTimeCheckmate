import requests
from lxml import etree
from objects import *
from book_site import BookSite
from PIL import Image
class LivrariaCultura(BookSite):
    def __init__(self):
        self.slug = 'lc'
        self.base = 'https://www3.livrariacultura.com.br/'
        self.search = 'busca/'

    def _construct_params_of_search(self, book_data):
        return {"ft":str(book_data)}

    def _find_results_of_search(self, root):
        return root.xpath("//div[@class='prateleiraProduto__informacao']/h2/a/@href")

    #region parse subfunctions
    def _find_book_format(self, root):
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

    def _find_book_image_url(self, root):
        try:
            book_image_url = root.xpath("//img[@id='image-main']/@src")[0]
            if book_image_url != None:
                return book_image_url
            else:
                return ""
        except:
            return ""

    def _find_book_image(self, url):
        try:
            rspns = requests.get(url, stream=True)
            rspns.raw.decode_content = True
            book_image = Image.open(rspns.raw)
            return book_image
        except:
            return None

    def _find_isbn_13(self, root):
        try:
            isbn_13 = root.xpath("//td[@class='value-field ISBN']")[0].text
            if isbn_13 != None:
                return isbn_13
            else:
                return ""
        except:
            return ""

    def _find_description(self, root):
        try:
            description = root.xpath("//td[@class='value-field Sinopse']")[0].text
            if description != None:
                return description
            else:
                return ""
        except:
            return ""

    def _find_title(self, root):
        try:
            title = root.xpath("//h1[@class='title_product']/div")[0].text
            if title != None:
                return title
            else:
                return ""
        except:
            return ""

    def _find_subtitle(self, root):
        try:
            subtitle = root.xpath("//span[@class='subtitle']")[0].text
            if subtitle != None:
                return subtitle
            else:
                return ""
        except:
            return ""

    def _find_authors(self, root):
        authors = root.xpath("//td[@class='value-field Colaborador']/text()")
        revised = []
        for a in authors:
            try:
                index = a.index(':')
            except:
                index = 0
            revised.append(a[index+1:])
        return revised

    def _find_ready_for_sale(self, root):
        return root.xpath("//button[@class='buy-in-page-button']") != []
    #endregion