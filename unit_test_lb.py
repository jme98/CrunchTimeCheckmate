from checkmate import *

lc = 'bible-commentary-the-gospel-of-john-2012895340/p'

slug = 'lc'
site = get_book_site(slug)
url = site.convert_book_id_to_url(lc)
sbd = site.get_book_data_from_site(url)
baseline = SiteBookData()

baseline.book_format = "DIGITAL"
baseline.book_image_url = "https://livrariacultura.vteximg.com.br/arquivos/ids/16063420-292-292/2012895340.jpg?v=637142714929230000"
baseline.book_image = site._find_book_image(baseline.book_image_url)
baseline.isbn_13 = "9788582182086"
baseline.description = "Bible Commentaries of J.C. Ryle on Gospel of John. A great volume to enlighten and strengthen all modern-day believers J.C. Ryle Anglican bishop of Liverpool.\nThoroughly evangelical in his doctrine and uncompromising in his principles, Ryle was a prolific writer, vigorous preacher, and faithful pastor. Charles Spurgeon considered him \"the best man in the Church of England.\""
baseline.title = "BIBLE COMMENTARY - THE GOSPEL OF JOHN"
baseline.subtitle = ""
baseline.series = ""
baseline.authors = ["RYLE, J.C."]

baseline.ready_for_sale = True
baseline.book_id = "bible-commentary-the-gospel-of-john-2012895340/p"
baseline.site_slug = "lc"
baseline.url = "https://www3.livrariacultura.com.br/bible-commentary-the-gospel-of-john-2012895340/p"
baseline.parse_status = "FULLY_PARSED"
print("Expected\n_______\n")
baseline.pr()
print("\n\n\nActual\n_______\n")
sbd.pr()
print("\n\n\nComparison: " + str(site.evaluate_potential_match(baseline, sbd)) + "%")