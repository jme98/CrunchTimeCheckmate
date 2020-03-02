import io
import requests
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

    parse_status = 'NO PARSE' # FULLY_PARSED(format, isbn, descr, title, authors), or UNSUCCESSFULL;
    try:
        book_format = root.xpath('.//div[@class="bookitem-secondary-metadata"]/h2')[0] # DIGITAL, PRINT, or AUDIOBOOK
        if book_format.text.find('eBook') != -1:
            book_format = 'E-Book'
        elif book_format.text.find('Audiobook') != -1:
            book_format = 'AudioBook'
        else:
            book_format = 'No Format Found'
        isbn_13 = root.xpath('.//div[@class="bookitem-secondary-metadata"]/ul/li[contains(text(), "ISBN:")]/span[@translate="no"]')[0].text # ISBN (may be converted from ISBN-10)
        description = root.xpath('.//div[@class="synopsis-description"]/descendant::*/text()') # book description fount at site
        description_content = ''
        for x in description:
            description_content += x + ' '
        title = root.xpath('.//span[@class="title product-field"]')[0].text #the title of the book
        authors = root.xpath('.//span[@class="authors product-field contributor-list"]/span[@class="visible-contributors"]/descendant::*/text()') # all authors for the work
        authors_content = ''
        for x in authors:
            authors_content += x + ', '
        parse_status = 'FULLY_PARSED'
    except:
        parse_status =  'UNSUCCESSFULL'





    try:
        series = root.xpath('.//span[@class="series product-field"]/span[@class="product-sequence-field"]/descendant::*/text()')[0] # all authors for the work
    except:
        series = 'none'

    try:    
        subtitle = root.xpath('.//span[@class="subtitle product-field"]')[0].text # the book's subtitle (if any)
    except:
        subtitle = 'No Subtitle'

#    book_id = book_id # page identifier (used to reconstruct direct page URL), MAY NOT BE ISBN!
    site_slug = 'https://www.kobo.com/us/en/' # slug for the BookSite
    book_image_url = 'https:' + root.xpath('.//img[@class="cover-image  notranslate_alt"]/@src')[0] # direct URL to cover
    book_image =  get_image(book_image_url)     # Pillow image of cover
    book_image.show()

    url = site_slug + book_id  # final, direct URL to the book page
#    content = "" #html content of the parsed page
    ready_for_sale = True  # boolean; is this book currently purchasable at this site?
    extra = {} # dictionary of any other relevant data provided by the BookSite


    
    return book_format + '\n' + isbn_13 + '\n' + description_content + '\n' + series + '\n' + title + '\n' + subtitle + '\n' + authors_content + '\n' + book_id + '\n' + site_slug + '\n' + url + '\n' + book_image_url


x = scrape_kb('ebook/i-am-n')
print(parse(x, 'ebook/i-am-n'))

y = scrape_kb('audiobook/the-warsaw-protocol')
print(parse(y, 'audiobook/the-warsaw-protocol'))

#audiobook/the-warsaw-protocol
