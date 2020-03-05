import requests
from lxml import etree
from objects import *
from book_site import BookSite
from PIL import Image
class TestBook(BookSite):
    def __init__(self):
        self.slug = 'tb'
        self.base = 'http://127.0.0.1:8000/'
        self.stripped = '127.0.0.1:8000'
        self.search = 'search/'

    def _construct_params_of_search(self, book_data):
        return {"q":str(book_data)}

    def _find_results_of_search(self, root):
        results = root.xpath("//a[@class='noColor']/@href")
        for result in results:
            result = results[1:]

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

    def _find_isbn_13(self, root):
        try:
            isbn_13 = root.xpath("//div[@class='col-sm-10 ']/p")[4].text[1:]
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
            title = root.xpath("//div[@class='col-sm-10 ']/h1")[0].text[12:]
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