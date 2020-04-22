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

    def __init__(self, isbn_13="", title="", authors=[]):
        self.isbn_13 = isbn_13
        self.title = title
        self.authors = authors

    def __str__(self):
        return_string = self.title
        return_string += " " + self.isbn_13
        for a in self.authors:
            return_string += " " + a
        return return_string.strip(".,' ")

    def pr(self):
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

    def to_json(self):
        description_lines = self.description.split("\n")
        description = ""
        for i in range(len(description_lines)):
            line = description_lines[i]
            if i != 0:
                description += "<br/>"
            description += line
        json_string = "{\n"
        json_string += f'    "book_format" : "{self.book_format}",\n'
        json_string += f'    "book_image_url" : "{self.book_image_url}",\n'
        json_string += f'    "isbn_13" : "{self.isbn_13}",\n'
        json_string += f'    "description" : "{description}",\n'
        json_string += f'    "series" : "{self.series}",\n'
        json_string += f'    "title" : "{self.title}",\n'
        json_string += f'    "subtitle" : "{self.subtitle}",\n'
        json_string += '    "authors" : [\n'
        for i in range(len(self.authors)):
            a = self.authors[i]
            if i != 0:
                json_string += ",\n"
            json_string += f'        "{a}"'
        json_string += "\n    ],\n"
        json_string += f'    "book_id" : "{self.book_id}",\n'
        json_string += f'    "site_slug" : "{self.site_slug }",\n'
        json_string += f'    "url" : "{self.url}",\n'
        json_string += f'    "ready_for_sale" : "{(str(self.ready_for_sale)).upper()}",\n'
        json_string += f'    "parse_status" : "{self.parse_status}",\n'
        json_string += '    "extras" : {\n'
        trailingComma = False
        for extra, value in self.extras.items():
            if trailingComma:
                json_string += ",\n"
            else:
                trailingComma = True
            json_string += f'        "{extra}" : "{str(value)}"'
        json_string += "\n    }\n"
        json_string += "}"
        return json_string

    def from_json(self, blob):
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
