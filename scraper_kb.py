import io
import requests
from objects import *
from lxml import etree
from PIL import Image
from _io import BytesIO

#basically copied from david for initial testing, thanks!
def scrape_kb(book_id):
    url = 'https://www.kobo.com/us/en/' + book_id
    response = requests.get(url)
    #open("kbSample.txt", "wb").write(requests.get(url).content)
    return response.content

def get_image(image_url):
    print(image_url)
    rspns = requests.get(image_url, stream=True)
    rspns.raw.decode_content = True
    return Image.open(rspns.raw)

def parse(content, book_id):
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    data = SiteBookData()

    data.parse_status = 'NO PARSE' # FULLY_PARSED(format, isbn, descr, title, authors), or UNSUCCESSFULL;
    try:
        data.book_format = root.xpath('.//div[@class="bookitem-secondary-metadata"]/h2')[0] # DIGITAL, PRINT, or AUDIOBOOK
        if data.book_format.text.find('eBook') != -1:
            data.book_format = 'E-Book'
        elif data.book_format.text.find('Audiobook') != -1:
            data.book_format = 'AudioBook'
        else:
            data.book_format = 'No Format Found'
        data.isbn_13 = root.xpath('.//div[@class="bookitem-secondary-metadata"]/ul/li[contains(text(), "ISBN:")]/span[@translate="no"]')[0].text # ISBN (may be converted from ISBN-10)
        description = root.xpath('.//div[@class="synopsis-description"]/descendant::*/text()') # book description fount at site
        data.description = ''
        for x in description:
            data.description += x + ' '
        data.title = root.xpath('.//span[@class="title product-field"]')[0].text #the title of the book
        authors = root.xpath('.//span[@class="authors product-field contributor-list"]/span[@class="visible-contributors"]/descendant::*/text()') # all authors for the work
        data.authors = ''
        for x in authors:
            data.authors += x + ', '
        data.parse_status = 'FULLY_PARSED'
    except:
        data.parse_status =  'UNSUCCESSFULL'


    try:
        data.series = root.xpath('.//span[@class="series product-field"]/span[@class="product-sequence-field"]/descendant::*/text()')[0] # all authors for the work
    except:
        data.series = 'none'

    try:    
        data.subtitle = root.xpath('.//span[@class="subtitle product-field"]')[0].text # the book's subtitle (if any)
    except:
        data.subtitle = 'No Subtitle'

    data.site_slug = 'https://www.kobo.com/us/en/' # slug for the BookSite
    try:
        data.book_image_url = 'https:' + root.xpath('.//img[@class="cover-image  notranslate_alt"]/@src')[0] # direct URL to cover
        data.book_image =  get_image(data.book_image_url)     # Pillow image of cover
    except:
        print('book image errors occured')
    # book_image.show()

    data.url = data.site_slug + book_id  # final, direct URL to the book page
    data.content = content  #html content of the parsed page
    data.book_id = book_id  # page identifier (used to reconstruct direct page URL), MAY NOT BE ISBN!
#  
    data.ready_for_sale = True  # boolean; is this book currently purchasable at this site?
    data.extra = {} # dictionary of any other relevant data provided by the BookSite

#set site book data object here
    

    
    return data

x = scrape_kb('ebook/i-am-n')
#print(parse(x, 'ebook/i-am-n'))
parse(x, 'ebook/i-am-n')
y = scrape_kb('audiobook/the-warsaw-protocol')
#print(parse(y, 'audiobook/the-warsaw-protocol'))
parse(y, 'audiobook/the-warsaw-protocol')
#audiobook/the-warsaw-protocol
