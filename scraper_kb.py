import requests
from lxml import etree
from objects import *
from book_site import BookSite
from PIL import Image
class Kobo(BookSite):
    def __init__(self):
        self.slug = 'kb'
        self.base = 'https://www.kobo.com/us/en/'
        self.search = 'search'
        
    def find_book_matches_at_site(self, book_data):
        search_string = book_data.title
        for a in book_data.authors:
            search_string += " " + a
        search_string.strip(".,' ")

        responses = []
        responses.append(requests.get(self.base + self.search, params=self._construct_params_of_search(search_string)))
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
            graded_results.append((result, self.evaluate_potential_match(book_data, result)))

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
        return root.xpath("//p[@class='title product-field']/a/@href")

    #region parse subfunctions
    def _find_book_format(self, root):
        try:
            book_format = root.xpath('.//div[@class="bookitem-secondary-metadata"]/h2')[0].text
            if book_format != None:
                if book_format[:9] == 'Audiobook':
                    return 'AUDIOBOOK'
                elif book_format[:5] == 'eBook':
                    return 'DIGITAL'
                else:
                    return 'PRINT'
            else:
                return ""
        except:
            return ""

    def _find_book_image_url(self, root):
        try:
            book_image_url = 'https:' + root.xpath('.//img[@class="cover-image  notranslate_alt"]/@src')[0]
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
            isbn_13 = root.xpath('.//div[@class="bookitem-secondary-metadata"]/ul/li[contains(text(), "ISBN:")]/span[@translate="no"]')[0].text
            if isbn_13 != None:
                return isbn_13
            else:
                return ""
        except:
            return ""

    def _find_description(self, root):
        try:
            descr = root.xpath('.//div[@class="synopsis-description"]/descendant::*/text()')
            description = ''
            for paragraph in descr:
                description += paragraph + '\n'

            if description != None:
                return description
            else:
                return ""

        except:
            return ""

    def _find_title(self, root):
        try:
            title = root.xpath('.//span[@class="title product-field"]')[0].text[2:]
            formatting = True
            if title != None:
                return title
            else:
                return ""
        except:
            return ""

    def _find_subtitle(self, root):
        try:
            subtitle = root.xpath('.//span[@class="subtitle product-field"]')[0].text[2:]
            if subtitle != None:
                return subtitle
            else:
                return ""
        except:
            return ""

    def _find_series(self, root):
        try:
            series = root.xpath('.//span[@class="series product-field"]/span[@class="product-sequence-field"]/descendant::*/text()')[0]
            if series != None:
                return series
            else:
                return ""
        except:
            return ""

    def _find_authors(self, root):
        return root.xpath('.//span[@class="authors product-field contributor-list"]/span[@class="visible-contributors"]/descendant::*/text()')

    def _find_ready_for_sale(self, root):
        try:
            purchasable = root.xpath('.//button[@class="purchase-action buy-now"]/span')
            return purchasable != []
        except:
            return ""
    #endregion