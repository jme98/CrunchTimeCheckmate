import requests, io
from lxml import etree
from objects import *
from book_site import BookSite
from PIL import Image
from datetime import datetime

class TestBook(BookSite):
    def __init__(self):
        self.slug = 'tb'
        self.base = 'http://127.0.0.1:8000/'
        self.stripped = '127.0.0.1:8000'
        self.search = 'TestBookStore/search/'

    def _construct_params_of_search(self, book_data):
        return {"q":str(book_data)}

    def _find_results_of_search(self, root):
        results = root.xpath("//a[@class='noColor']/@href")
        try:
            results = results[1:]
            full_results = []
            for result in results:
                full_results.append(self.base + result[1:])
            return full_results
        except:
            return results

    #region parse subfunctions
    def _find_book_format(self, root):
        try:
            book_format = root.xpath("//strong[text()='Format:']")[0].tail[1:]
            if book_format != None:
                if book_format[0] == "E":
                    return "DIGITAL"
                elif book_format[0] == "A" and format_code not in ["A205", "A206", "A211", "A212"]:
                    return "AUDIOBOOK"
                elif book_format[0] == "B":
                    return "PRINT"
                else:
                    return ""
            else:
                return ""
        except:
            return ""

    def _find_isbn(self, root):
        try:
            isbn = root.xpath("//strong[text()='ISBN 13:']")[0].tail[1:]
            if isbn != None:
                return isbn
            else:
                return ""
        except:
            return ""

    def _find_description(self, root):
        try:
            description = str(root.xpath("//p[@class='b:description']")[0])
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
                if series_name == "N/A":
                    return "" 
                else:
                    return series
            else:
                return ""
        except:
            return ""

    def _find_authors(self, root):
        authors = root.xpath("//ul/p/text()")
        """ authors_list = []
        for a in authors:
            given_name = a.split()[0]
            surname = a.split()[1]
            authors_list.append({given_name, surname})
        return authors_list """
        return authors

    def _find_ready_for_sale(self, root):
        return False

    def _parse_date_string(self, date_string):
        truncate_index = date_string.rfind(",") #locate the comma that comes after the year
        fixed_string = date_string[1:truncate_index] #remove the offending comma and everything after it, as well as the leading whitespace
        date_object = datetime.strptime(fixed_string, "%b. %d, %Y") #convert to a datetime object via careful formatting
        return date_object

    def _find_price(self, etree_root):
        xpath = "//p/strong[normalize-space(text()) = 'Price:']/following-sibling::text()"
        try:
            price = etree_root.xpath(xpath)[0]
            price = price[1:] #remove leading whitespace
            final_string = "$"
            final_string = final_string + price
            return final_string
        except:
            return ""

    def _find_release_date(self, etree_root):
        xpath = "//p/strong[normalize-space(text()) = 'Release Date:']/following-sibling::text()"
        try:
            date_string = etree_root.xpath(xpath)[0]
            release_date = self._parse_date_string(date_string)
            return release_date
        except:
            return ""

    def _find_extras(self, root):
        extras = {}
        extras["price"] = self._find_price(root)
        extras["release_date"] = self._find_release_date(root)
        return extras
    #endregion
