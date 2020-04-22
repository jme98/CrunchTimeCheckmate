from checkmate import *

isbn = '9788582182086'
title = 'BIBLE COMMENTARY - THE GOSPEL OF JOHN'
authors = ['RYLE, J.C.']
data = SiteBookData(isbn, title)

slug = 'lc'
site = get_book_site(slug)

matches = site.find_book_matches_at_site(data)

for match in matches:
    if match[1] > 0:
        print(match[0].title + " (" + str(match[1]) + ")")