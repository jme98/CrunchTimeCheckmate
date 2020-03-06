import requests
from lxml import etree
from objects import *
from book_site import BookSite
from PIL import Image

class GoogleBooks(BookSite):
    def __init__(self):
        self.slug = 'gb'
        self.base = 'https://www.google.com/'
        self.search = 'search'

    def _construct_params_of_search(self, book_data):
        return {
            "tbm":"bks",
            "q":str(book_data)
        }

#DON"T FORGET
    def _find_results_of_search(self, root):
        p = root.xpath(".//div[@class='ZINbbc xpd O9g5cc uUPGi']/div[@class='x54gtf']/following-sibling::div/a/@href")
        return p

    #region parse subfunctions
    def _find_book_format(self, root):
        try:
            p = root.xpath(".//a[@id='gb-get-book-content']")[0].text
            if "buy" in p.lower() and "ebook" in p.lower():
                return "DIGITAL"
            elif "get print" in p.lower():
                return "PRINT"
            elif "audio" in p.lower():
                return "AUDIOBOOK"
            else:
                return ""
        except:
            return ""

    def _find_book_image_url(self, root):
        try:
            biu = root.xpath(".//link[@rel='image_src']")[0].get("href")
            if biu != None:
                return biu
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
            stuff = root.xpath(".//span[@dir='ltr']")
            count = 0
            isbn_start = 0
            for i in stuff:
                if ("ISBN" in i.text):
                    isbn_start = count + 1
                count = count + 1
            isbn_str = ""
            ready = 0
            for i in stuff[isbn_start].text:
                if i is " ":
                    ready = 1
                elif ready == 1:
                    isbn_str = isbn_str + i

            return isbn_str
        except:
            return ""

    def _find_description(self, root):
        try:
            desc = root.xpath(".//meta[@name='description']")[0].get("content")
            if desc != None:
                return desc
            else:
                return ""
        except:
            return ""

    def _find_title(self, root):
        try:
            t = root.xpath(".//meta[@name='title']")[0].get("content")
            if t != None:
                return t
            else:
                return ""
        except:
            return ""

    def _find_subtitle(self, root):
        try:
            sub = root.xpath(".//span[@class='subtitle']/span")[0].text
            if sub != None:
                return sub
            else:
                return ""
        except:
            return ""

    def _find_authors(self, root):
        stuff = root.xpath("//span[@dir='ltr']")
        count = 0
        author_start = 0
        aList = []
        for i in stuff:
            if ("author" in i.text.lower()):
                author_start = count + 1
            count = count + 1
        
        while author_start != 0 and author_start != len(stuff) and "edition" not in stuff[author_start].text.lower() and "publisher" not in stuff[author_start].text.lower() and "illustrated by" not in stuff[author_start].text.lower():
            aList.append(stuff[author_start].text)
            author_start = author_start + 1

        if len(aList) == 0:
            stuff = root.xpath("//span[@class='addmd']")
            for i in stuff:
                aList.append(i.text[3:])
        return aList

    def _find_ready_for_sale(self, root):
        try:
            p = root.xpath(".//a[@id='gb-get-book-content']")[0].text
            rfs = False
            if "buy" in p.lower() or "get print" in p.lower():
                rfs = True
            return rfs
        except:
            return None 

    def _find_series(self, root):
        try:
            stuff = root.xpath(".//span[@dir='ltr']")
            s = ""
            count = 0
            for i in stuff:
                if "book" in i.text[0:4].lower() and i.text[5].isdigit():
                    s = i.text
                count = count + 1
            if s != None:
                return s
            else:
                return ""
        except:
            return ""   
#endregion