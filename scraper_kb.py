import io
import requests
from objects import *
from lxml import etree
from PIL import Image
from _io import BytesIO

def scrape_kb(book_id):
    url = 'https://www.kobo.com/us/en/' + book_id
    response = requests.get(url)
    return response.content

def get_image(image_url):
    print(image_url)
    rspns = requests.get(image_url, stream=True)
    rspns.raw.decode_content = True
    return Image.open(rspns.raw)

#terms is assumed to contain a string of search terms separated by whitespace characters
#tested: gets the proper page
def search(terms):
    url = 'https://www.kobo.com/us/en/'
    for x in terms:
        if x.isspace():
            x = '+'
    url += 'search?query=' + terms
    response = requests.get(url)
    print(response.content)

#def evaluate_potential_match(self, baseline, match):
#    value = 0
#    if baseline.isbn_13 == match.isbn_13:
#        value += 1/2
#    if baseline.title == match.title:
#        value += 1/4
#    if baseline.authors == match.authors:
#        value += 1/8
#    if baseline.book_format == match.book_format:
#        value += 1/16
#    if baseline.subtitle == match.subtitle:
#        value += 1/32
#    if baseline.series == match.series:
#        value += 1/64
#    if baseline.description == match.description:
#        value += 1/128
#    if baseline.book_image == match.book_image:
#        value += 1/128
#    return value

def parse(content, book_id):
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    data = SiteBookData()

    try:
        data.book_format = root.xpath('.//div[@class="bookitem-secondary-metadata"]/h2')[0]
        if data.book_format.text.find('eBook') != -1:
            data.book_format = 'E-Book'
        elif data.book_format.text.find('Audiobook') != -1:
            data.book_format = 'AudioBook'
        else:
            data.book_format = 'No Format Found'
        data.isbn_13 = root.xpath('.//div[@class="bookitem-secondary-metadata"]/ul/li[contains(text(), "ISBN:")]/span[@translate="no"]')[0].text
        description = root.xpath('.//div[@class="synopsis-description"]/descendant::*/text()')
        data.description = ''
        for x in description:
            data.description += x + ' '
        data.title = root.xpath('.//span[@class="title product-field"]')[0].text
        authors = root.xpath('.//span[@class="authors product-field contributor-list"]/span[@class="visible-contributors"]/descendant::*/text()')
        data.authors = ''
        for x in authors:
            data.authors += x + ', '
        data.parse_status = 'FULLY_PARSED'
    except:
        data.parse_status =  'UNSUCCESSFULL'

    try:
        data.series = root.xpath('.//span[@class="series product-field"]/span[@class="product-sequence-field"]/descendant::*/text()')[0]
    except:
        data.series = 'None'

    try:    
        data.subtitle = root.xpath('.//span[@class="subtitle product-field"]')[0].text
    except:
        data.subtitle = 'No Subtitle'

    data.site_slug = 'https://www.kobo.com/us/en/'
    try:
        data.book_image_url = 'https:' + root.xpath('.//img[@class="cover-image  notranslate_alt"]/@src')[0]
        data.book_image =  get_image(data.book_image_url)
    except:
        print('book image errors occured')
    
    data.url = data.site_slug + book_id
    data.content = content
    data.book_id = book_id
    data.ready_for_sale = True
    data.extra = {}

    return data

#test cases:
#x = scrape_kb('ebook/i-am-n')
#parse(x, 'ebook/i-am-n')
#y = scrape_kb('audiobook/the-warsaw-protocol')
#parse(y, 'audiobook/the-warsaw-protocol')
search('i am n')
