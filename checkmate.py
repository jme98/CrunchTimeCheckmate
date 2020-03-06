from scraper_lc import LivrariaCultura
from scraper_sd import Scribd
from scraper_kb import Kobo
from scraper_gb import GoogleBooks
from scraper_tb import TestBook
from objects import SiteBookData

def get_book_site(slug):
    if slug == 'lc':
        return LivrariaCultura()
    elif slug == 'sd':
        return Scribd()
    elif slug == 'kb':
        return Kobo()
    elif slug == 'gb':
        return GoogleBooks()
    elif slug == 'tb':
        return TestBook()