import requests
from lxml import etree
from objects import *
from book_site import BookSite
from PIL import Image
class Scribd(BookSite):
    def __init__(self):
        self.slug = 'sd'
        self.base = 'https://www.scribd.com/'
        self.search = 'search'

    #overriding super function because isbn-13 and title/author cannot be searched together on scribd
    def find_book_matches_at_site(self, book_data):
        mystr = book_data.title
        for a in book_data.authors:
            mystr += " " + a
        mystr.strip(".,' ")

        responses = []
        responses.append(requests.get(self.base + self.search, params=self._construct_params_of_search(mystr)))
        responses.append(requests.get(self.base + self.search, params=self._construct_params_of_search(book_data.isbn_13)))
        roots = []
        roots.append(etree.fromstring(responses[0].content, etree.HTMLParser()))
        roots.append(etree.fromstring(responses[1].content, etree.HTMLParser()))
        links = self._find_results_of_search(roots[0])
        links += self._find_results_of_search(roots[1])
        links = list(dict.fromkeys(links))

        results = []
        graded_results = []
        for l in links:
            results.append(self.get_book_data_from_site(l))
        for result in results:
            graded_results.append((result.title, self.evaluate_potential_match(book_data, result)))

        empty = True
        while (empty):
            try:
                graded_results.remove(('', 0))
            except:
                empty = False

        return graded_results

    def _construct_params_of_search(self, book_data):
        return {"query":str(book_data)}

    def _find_results_of_search(self, root):
        urls = []
        script = root.xpath("//script[@src='https://apis.google.com/js/platform.js?onload=googleOnLoad']/following-sibling::script")[0].text
        pre = script.find('book_preview_url')
        while (pre != -1):
            first = script.find('https://www.scribd.com/', pre)
            post = script.find('}', first)
            url = script[first:post-1]
            if (url != ""):
                urls.append(url)
            pre = script.find('book_preview_url', post)
        return urls


    #region parse subfunctions
    def _find_book_format(self, root):
        try:
            book_format = root.xpath("//meta[@property='og:type']/@content")[0]
            if book_format != None:
                if book_format == 'book':
                    return 'DIGITAL'
                else:
                    return 'AUDIOBOOK'
            else:
                return ""
        except:
            return ""
        
    def _find_book_image_url(self, root):
        try:
            book_image_url = root.xpath("//meta[@property='og:image']/@content")[0]
            if book_image_url != None:
                return book_image_url
            else:
                return ""
        except:
            return ""

    def _find_book_image(self, url):
        try:
            rspns = requests.get(url, stream=True)
            rspns.raw.decode_content = True
            book_image = Image.open(rspns.raw)
            return book_image
        except:
            return None

    def _find_isbn(self, root):
        try:
            isbn_13 = root.xpath("//meta[@property='books:isbn']/@content")[0]
            if isbn_13 != None:
                return isbn_13
            else:
                return ""
        except:
            return ""

    def _find_description(self, root):
        try:
            description = root.xpath("//meta[@name='twitter:description']/@content")[0]
            if description != None:
                return description
            else:
                return ""
        except:
            return ""

    def _find_title(self, root):
        try:
            title = root.xpath("//meta[@property='og:title']/@content")[1]
            if title != None:
                return title
            else:
                return ""
        except:
            return ""

    def _find_subtitle(self, root):
        try:
            subtitle = root.xpath("//span[@class='subtitle']")[0].text
            if subtitle != None:
                return subtitle
            else:
                return ""
        except:
            return ""

    def _find_authors(self, root):
        authors = root.xpath("//span[@class='author']/descendant::*/text()")
        if len(authors) > 1:
            return authors[1:]
        else:
            return []

    def _find_ready_for_sale(self, root):
        return True
    #endregion