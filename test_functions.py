from scraper_lc import LivrariaCultura
from scraper_sd import Scribd
from scraper_gb import GoogleBooks

from objects import SiteBookData

def get_book_site(slug):
    if slug == 'lc':
        return LivrariaCultura()
    elif slug == 'sd':
        return Scribd()
    elif slug == 'gb':
        return GoogleBooks()

#sample book_id from each site:
lc = 'bible-commentary-the-gospel-of-john-2012895340/p'
sd = 'book/295105408/The-MacArthur-Study-Bible'
gb = "books?id=LhTuQAAACAAJ"


slug = 'gb'
site = get_book_site(slug)
url = site.convert_book_id_to_url(gb)
sbd = site.get_book_data_from_site(url)
#print(site.find_book_matches_at_site(sbd))

#open("lcsample2.txt", "wb").write(site.find_book_matches_at_site(sbd))
sbd.pr()