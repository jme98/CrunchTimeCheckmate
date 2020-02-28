import requests
from lxml import etree

def scrape_gb(book_id):
    url = 'https://books.google.com/books?id=' + book_id
    response = requests.get(url)
    print(response.content)

scrape_gb("LhTuQAAACAAJ")
print("hey listen")