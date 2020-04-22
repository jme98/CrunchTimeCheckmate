"""
BookSites are referenced as follows:
   tb = TestBookStore
   kb = Kobo
   gb = Google Books
   lc = LivrariaCultura
   sd = Scribd
   ab = Audiobooks.com
"""

import string
import json, requests
from PIL import Image

class SiteBookData:
    """Book details as gathered from a specific entry at a specific book site"""
    book_format = "" # DIGITAL, PRINT, or AUDIOBOOK
    book_image = None # Pillow image of cover
    book_image_url = "" # direct URL to cover
    isbn_13 = "" # ISBN (may be converted from ISBN-10)
    description = "" # book description fount at site
    series = "" # the series the book is part of (if any)
    title = "" #the title of the book
    subtitle = "" # the book's subtitle (if any)
    authors = [] # all authors for the work
    book_id = "" # page identifier (used to reconstruct direct page URL), MAY NOT BE ISBN!
    site_slug = "" # slug for the BookSite
    parse_status = "" # FULLY_PARSED or UNSUCCESSFUL
    url = "" # final, direct URL to the book page
    page_content = "" #html content of the parsed page
    ready_for_sale = False # boolean; is this book currently purchasable at this site?
    extras = {} # dictionary of any other relevant data provided by the BookSite
    ready_for_sale_str = "false" #string version of the ready_for_sale boolean

    def __init__(self, isbn = '', title = '', authors = []):
        if len(isbn) == 10:
            nine_digits = isbn[0:9] #slice off the old check digit
            final_isbn = "978"
            final_isbn += nine_digits
            final_isbn += self._calc_check_digit(final_isbn)
            self.isbn_13 = final_isbn
        else:
            self.isbn_13 = isbn
        self.title = title
        self.authors = authors

    def __str__(self):
        return_string = self.title
        return_string += " " + self.isbn_13
        for a in self.authors:
            return_string += " " + a
        return return_string.strip(".,' ")

    def pr(self):
        """Prints all identifying details of the book"""
        print_string = "Format: " + self.book_format + "\n"
        print_string += "Image Url: " + self.book_image_url + "\n"
        print_string += "ISBN-13: " + self.isbn_13 + "\n\n"
        print_string += "Description: \n" + self.description + "\n\n"
        print_string += "Series: " + self.series + "\n"
        print_string += "Title: " + self.title + "\n"
        print_string += "Subtitle: " + self.subtitle + "\n"
        print_string += "Authors: \n"
        for a in self.authors:
            print_string += "    " + a.strip("., ") + "\n"
        print_string += "Book ID: " + self.book_id + "\n"
        print_string += "Site Slug: " + self.site_slug + "\n"
        print_string += "URL: " + self.url + "\n"
        print_string += "RFS: " + str(self.ready_for_sale) + "\n"
        print_string += "Parse Status: " + self.parse_status + "\n"
        print_string += "Extras:\n"
        for extra, value in self.extras.items():
            print_string += "    " + extra + ": " + str(value) + "\n"
        print_string += "\n\n"
        print(print_string)
        try:
            self.book_image.show()
        except:
            print("No cover image available.")

    def _calc_check_digit(self, isbn_string):
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

'''
get_book_site(slug)
# type: (str) -> BookSite
"""Given a booksite slug, return a BookSite object corresponding to the slug"""

    def from_json(self, blob):
        """Converts SiteBookData JSON
        in description, replaces '<br/>' with '\\n'
        """
        json_dict = json.loads(blob)

        self.book_format = json_dict.get("book_format", "")
        self.book_image_url = json_dict.get("book_image_url", "")
        if self.book_image_url != "":
            rspns = requests.get(self.book_image_url, stream=True)
            rspns.raw.decode_content = True
            self.book_image = Image.open(rspns.raw)
        self.isbn_13 = json_dict.get("isbn_13", "")
        self.description = json_dict.get("description", "")

        description_lines = self.description.split("<br/>")
        description = ""
        for i in range(len(description_lines)):
            line = description_lines[i]
            if i != 0:
                description += "\n"
            description += line
        self.description = description

        self.series = json_dict.get("series", "")
        self.title = json_dict.get("title", "")
        self.subtitle = json_dict.get("subtitle", "")
        self.authors = json_dict.get("authors", [])
        self.book_id = json_dict.get("book_id", "")
        self.site_slug = json_dict.get("site_slug", "")
        self.parse_status = json_dict.get("parse_status", "")
        self.url = json_dict.get("url", "")
        self.ready_for_sale = json_dict.get("ready_for_sale", False)
        self.extras = json_dict.get("extras", {})
        
    def ready_for_sale_string(self):
        if self.ready_for_sale:
            return "true"
        else:
            return "false"
