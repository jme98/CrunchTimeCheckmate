"""
BookSites are referenced as follows:
   tb = TestBookStore
   kb = Kobo
   gb = Google Books
   lc = LivrariaCultura
   sd = Scribd
"""

import string

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
