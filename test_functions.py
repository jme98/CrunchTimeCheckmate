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

#sample book_id from each site:
lc = 'bible-commentary-the-gospel-of-john-2012895340/p'
sd = 'book/295105408/The-MacArthur-Study-Bible'
kb = 'ebook/hello-a-trilogy-1'
gb = 'books?id=LhTuQAAACAAJ'
tb = 'TestBookStore/book_detail/781524243456/'


slug = 'tb'
site = get_book_site(slug)
url = site.convert_book_id_to_url(tb)
sbd = site.get_book_data_from_site(url)
print(sbd.description)
#print(site.find_book_matches_at_site(sbd))

#open("sdsample2.txt", "wb").write(site.find_book_matches_at_site(sbd))
