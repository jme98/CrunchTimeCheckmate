from checkmate import *

#sample book_id from each site:
lc = 'bible-commentary-the-gospel-of-john-2012895340/p'
sd = 'book/295105408/The-MacArthur-Study-Bible'
kb = 'ebook/hello-a-trilogy-1'
gb = 'books?id=30ZuZjVP7V0C'
tb = 'TestBookStore/book_detail/781524243456/'

#Test Suite
slug = 'kb'
site = get_book_site(slug)
url = site.convert_book_id_to_url(kb)
sbd = site.get_book_data_from_site(url)

sbd2 = SiteBookData()
sbd2.from_json(sbd.to_json())
print(sbd.to_json())