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
            book_format = root.xpath("//strong[text()='Format:']")[0].tail[1:]
            if book_format != None:
                if book_format == 'E101':
                    return 'DIGITAL'
                elif book_format == 'ePub':
                    return 'PRINT'
                else:
                    return 'AUDIOBOOK'
            else:
                return ""
        except:
            return ""

    def _find_isbn_13(self, root):
        try:
            title = root.xpath("//strong[text()='ISBN 13:']")[0].tail[1:]
            if title != None:
                return title
            else:
                return ""
        except:
            return ""

    def _find_description(self, root):
        try:
            description = str(root.xpath("//strong[text()='Book Description:']/parent::p/following-sibling::p/p")[0])
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
            subtitle = root.xpath("//strong[text()='Subtitle:']")[0].tail[1:]
            if subtitle != None:
                return subtitle
            else:
                return ""
        except:
            return ""

    def _find_series(self, root):
        try:
            series = root.xpath("//strong[text()='Series Name:']")[0].tail[1:]
            if series != None:
                return series
            else:
                return ""
        except:
            return ""

    def _find_authors(self, root):
        return root.xpath("//ul/p/text()")

    def _find_ready_for_sale(self, root):
        return False
    #endregion