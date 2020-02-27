"""
BookSites are referenced as follows:
   tb = TestBookStore
   kb = Kobo
   gb = Google Books
   lc = LivrariaCultura
   sd = Scribd
"""

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


'''
get_book_site(slug)
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
