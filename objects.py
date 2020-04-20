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
    extra = {} # dictionary of any other relevant data provided by the BookSite

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
        mystr += "Parse Status: " + self.parse_status + "\n\n\n"
        print(mystr)
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

book_site.get_book_data_from_site(url)
# type: (str) -> SiteBookData
"""Given a direct link to a book page at a site, parse it and return the SiteBookData of the info"""

book_site.find_book_matches_at_site(book_data)
# type: (SiteBookData) -> List[Tuple[SiteBookData, float]]
"""Given a SiteBookData, search for the book at the ‘book_site’ site and provide a list of likely matches paired with how good of a match it is (1.0 is an exact match).
   This should take into account all the info we have about a book, including the cover."""

book_site.convert_book_id_to_url(book_id)
# type: (str) -> str
"""Given a book_id, return the direct URL for the book."""
'''
