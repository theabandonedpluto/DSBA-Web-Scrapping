# This program allows for playing with xpaths extraction,
# and testing them for specific sites.
from scrapy import Selector
from urllib import request
import pandas as pd

url = 'https://www.libristo.pl/books-in-english/humanities.html'
html = request.urlopen(url)
sel = Selector(text=html.read(), type="html")

xpath = '//ol[@class="LST"]/li'
print(len(sel.xpath(xpath).getall()))


