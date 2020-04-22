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
        mystr = self.title
        mystr += " " + self.isbn_13
        for a in self.authors:
            mystr += " " + a
        return mystr.strip(".,' ")

    def pr(self):
        mystr = "Format: " + self.book_format + "\n"
        mystr += "Image Url: " + self.book_image_url + "\n"
        mystr += "ISBN-13: " + self.isbn_13 + "\n\n"
        mystr += "Description: \n" + self.description + "\n\n"
        mystr += "Series: " + self.series + "\n"
        mystr += "Title: " + self.title + "\n"
        mystr += "Subtitle: " + self.subtitle + "\n"
        mystr += "Authors: \n"
        for a in self.authors:
            mystr += "    " + a.strip("., ") + "\n"
        mystr += "Book ID: " + self.book_id + "\n"
        mystr += "Site Slug: " + self.site_slug + "\n"
        mystr += "URL: " + self.url + "\n"
        mystr += "RFS: " + str(self.ready_for_sale) + "\n"
        mystr += "Parse Status: " + self.parse_status + "\n"
        mystr += "Extras:\n"
        for extra, value in self.extras.items():
            mystr += "    " + extra + ": " + str(value) + "\n"
        mystr += "\n\n"
        print(mystr)
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
        mystr = "{\n"
        mystr += f'    "book_format" : "{self.book_format}",\n'
        mystr += f'    "book_image_url" : "{self.book_image_url}",\n'
        mystr += f'    "isbn_13" : "{self.isbn_13}",\n'
        mystr += f'    "description" : "{description}",\n'
        mystr += f'    "series" : "{self.series}",\n'
        mystr += f'    "title" : "{self.title}",\n'
        mystr += f'    "subtitle" : "{self.subtitle}",\n'
        mystr += '    "authors" : [\n'
        for i in range(len(self.authors)):
            a = self.authors[i]
            if i != 0:
                mystr += ",\n"
            mystr += f'        "{a}"'
        mystr += "\n    ],\n"
        mystr += f'    "book_id" : "{self.book_id}",\n'
        mystr += f'    "site_slug" : "{self.site_slug }",\n'
        mystr += f'    "url" : "{self.url}",\n'
        mystr += f'    "ready_for_sale" : "{(str(self.ready_for_sale)).upper()}",\n'
        mystr += f'    "parse_status" : "{self.parse_status}",\n'
        mystr += '    "extras" : {\n'
        trailingComma = False
        for extra, value in self.extras.items():
            if trailingComma:
                mystr += ",\n"
            else:
                trailingComma = True
            mystr += f'        "{extra}" : "{str(value)}"'
        mystr += "\n    }\n"
        mystr += "}"
        return mystr

    def from_json(self, blob):
        jdict = json.loads(blob)

        self.book_format = jdict.get("book_format", "")
        self.book_image_url = jdict.get("book_image_url", "")
        if self.book_image_url != "":
            rspns = requests.get(self.book_image_url, stream=True)
            rspns.raw.decode_content = True
            self.book_image = Image.open(rspns.raw)
        self.isbn_13 = jdict.get("isbn_13", "")
        self.description = jdict.get("description", "")

        description_lines = self.description.split("<br/>")
        description = ""
        for i in range(len(description_lines)):
            line = description_lines[i]
            if i != 0:
                description += "\n"
            description += line
        self.description = description

        self.series = jdict.get("series", "")
        self.title = jdict.get("title", "")
        self.subtitle = jdict.get("subtitle", "")
        self.authors = jdict.get("authors", [])
        self.book_id = jdict.get("book_id", "")
        self.site_slug = jdict.get("site_slug", "")
        self.parse_status = jdict.get("parse_status", "")
        self.url = jdict.get("url", "")
        self.ready_for_sale = jdict.get("ready_for_sale", False)
        self.extras = jdict.get("extras", {})
