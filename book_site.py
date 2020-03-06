import requests
from lxml import etree
from objects import *
from PIL import Image
class BookSite:
    #region fields
    slug = '' #2-letter abbreviation for booksite
    base = '' #home-page url for booksite
    stripped = '' #same as 'base', but stripped of surrounding 'https://' and '/'
    search = '' #extension to 'base' used for making book searches
    #endregion

    def __init__(self):
        self.slug = 'bs'
        self.base = 'https://book.site.url/'
        self.search = 'find/'

    def get_book_data_from_site(self, url):
        response = requests.get(url)
        root = etree.fromstring(response.content, etree.HTMLParser())
        data = SiteBookData()

        data.book_format = self._find_book_format(root)
        data.book_image_url = self._find_book_image_url(root)
        data.book_image = self._find_book_image(data.book_image_url)
        data.isbn_13 = self._format_isbn(self._find_isbn(root))
        data.description = self._find_description(root)
        data.title = self._find_title(root)
        data.subtitle = self._find_subtitle(root)
        data.series = self._find_series(root)
        data.authors = self._find_authors(root)
        
        data.ready_for_sale = self._find_ready_for_sale(root)
        data.book_id = url[len(self.base):]
        data.site_slug = self.slug
        data.url = url
        data.content = response.content
        data.parse_status = self._find_parse_status(data)
        data.extras = self._find_extras(root)
        
        return data

    def find_book_matches_at_site(self, book_data):
        response = requests.get(self.base + self.search, params=self._construct_params_of_search(book_data))
        open("rando.txt", "wb").write(response.content)
        root = etree.fromstring(response.content, etree.HTMLParser())
        links = self._find_results_of_search(root)
        results = []
        graded_results = []
        for l in links:
            results.append(self.get_book_data_from_site(l))
        for result in results:
            graded_results.append((result, self.evaluate_potential_match(book_data, result)))

        return graded_results

    def evaluate_potential_match(self, baseline, match):
        value = 0
        prop = 1
        if baseline.isbn_13 != "":
            prop *= 2
            if baseline.isbn_13 == match.isbn_13:
                value += 1/prop
        if baseline.title != "":
            prop *= 2
            if baseline.title == match.title:
                value += 1/prop
        if baseline.authors != []:
            prop *= 2
            if baseline.authors == match.authors:
                value += 1/prop
        if baseline.book_format != "":
            prop *= 2
            if baseline.book_format == match.book_format:
                value += 1/prop
        if baseline.subtitle != "":
            prop *= 2
            if baseline.subtitle == match.subtitle:
                value += 1/prop
        if baseline.series != "":
            prop *= 2
            if baseline.series == match.series:
                value += 1/prop
        if baseline.description != "":
            prop *= 2
            if baseline.description == match.description:
                value += 1/prop
        if baseline.book_image != None:
            prop *= 2
            if baseline.book_image == match.book_image:
                value += 1/prop
        if value > 0:
            value += 1/prop
        return value

    def convert_book_id_to_url(self, book_id):
        return self.base + book_id


    def _construct_params_of_search(self, book_data):
        return {}

    def _find_results_of_search(self, root):
        return []

    #region parse subfunctions
    def _find_parse_status(self, data):
        if data.book_format != "" and data.isbn_13 != "" and data.description != "" and data.title != "" and data.authors != []:
            return "FULLY_PARSED"
        else:
            return "UNSUCCESSFUL"

    def _find_book_format(self, root):
        return "NO_FORMAT"

    def _find_book_image_url(self, root):
        return ""

    def _find_book_image(self, url):
        return None

    def _find_isbn(self, root):
        return ""

    def _find_description(self, root):
        return ""

    def _find_title(self, root):
        return ""

    def _find_subtitle(self, root):
        return ""

    def _find_series(self, root):
        return ""

    def _find_authors(self, root):
       return []

    def _find_ready_for_sale(self, root):
        return False
    
    def _find_extras(self, root):
        return {}

    def _format_isbn(self, isbn):
        if len(isbn) == 13:
            return isbn
        elif len(isbn) == 10:
            nine_digits = isbn[0:9] #slice off the old check digit
            final_isbn = "978"
            final_isbn.append(nine_digits)
            final_isbn.append(calc_check_digit(final_isbn))
            return final_isbn
        else:
            return None

    #endregion