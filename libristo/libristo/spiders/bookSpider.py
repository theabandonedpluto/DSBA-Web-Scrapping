import scrapy
from scrapy import Selector
import re
import pandas as pd
from timeit import default_timer as timer

start = timer()

# page limit parameter: if True, only 100 links will be crawled
page_limit = False

# the Book class of the scraped item, with defined features to scrap
class Book(scrapy.Item):
    title = scrapy.Field()
    author_year = scrapy.Field()
    lang = scrapy.Field()
    cover = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()


class LibristoSpider(scrapy.Spider):
    # name of the spider, called from bash 
    name = "bookSpider"
    allowed_domains = ["www.libristo.pl"]
    start_urls = ["http://www.libristo.pl/"]

    # class constructor initiated, with default pages attribute equal to 500
    def __init__(self, pages=500): 

        if page_limit: 
            self.pages = 100
        else: 
            self.pages = pages
            
        try:
            with open("links.csv", "rt") as f:
                cat_url= [url.strip() for url in f.readlines()][1:]
                print('Links to be crawled:', cat_url)
            
            # initiate empty list for urls to crawl 
            self.start_urls = []

            for url in cat_url: 
                page_url = [f'{url}_{i}.html' for i in range(1, int(self.pages)+1)]
                self.start_urls += page_url

        except: 
            self.start_urls = []


        # define empty list of books attribute
        self.books = []

    def parse(self, response):

        # first, select the info box of a book separately 
        books_list = response.xpath('//ol[@class="LST"]/li').getall()

        for k in books_list: 
            
            sel = Selector(text = k)

            
            title_xpath = '//div[@class = "LST_inf"]/h3/a/text()'
            author_year_xpath = '//div[@class = "LST_inf"]/h4/text()'
            lang_xpath = '//div[@class = "LST_inf"]/p[1]/text()'
            cover_xpath = "//p[strong[text()='Binding']]/text()"
            link_xpath = '//div[@class = "LST_inf"]/h3/a//@href'
            price_xpath = '//div[@class = "LST_buy"]/p/strong/text()'
            discount_xpath = '//li/div[@class="LST_buy"]/div[1]/text()'

            # for each book, retrieve xpath 
            title = sel.xpath(title_xpath).get()
            author_year = sel.xpath(author_year_xpath).get()
            lang = sel.xpath(lang_xpath).get()
            cover = sel.xpath(cover_xpath).get()
            link = sel.xpath(link_xpath).get()
            price = sel.xpath(price_xpath).get()
            discount = sel.xpath(discount_xpath).get()
        
            # store retrived data in a Book dictionary
            b = Book()
            b['title'] = title
            b['author_year'] = author_year
            b['lang'] = lang
            b['cover'] = cover
            b['link'] = link
            b['price'] = price
            b['discount'] = discount

            # append retrived info of a book to a list attribute self.books
            self.books.append(b)

    def closed(self, reason):
        
        # Create a DataFrame using the scraped data
        df = pd.DataFrame(self.books, columns=['title', 'author_year', 'lang', 'cover', 'link', 'price', 'discount'])
        
        # rename title 
        df.rename({'title': 'Title'}, axis=1, inplace=True)

        # extracting the author and years
        df['Author'] = [item.split("|")[0].strip() if (isinstance(item, str) and "|" in item) else "-" for item in df['author_year']]
        df['Year'] = [item[-4:] for item in df['author_year']]
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0)

        # Tidy the values of the 'language' and 'cover' columns
        df['Language'] = [item.split(": ")[1].strip() if (isinstance(item, str) and ":" in item) else "-" for item in df['lang']]
        df['CoverType'] = [item.split(": ")[1].strip() if ":" in item else "-" for item in df['cover']]

        # Add 'https://www.libristo.pl' to 'link' column values
        df['Links'] = ["https://www.libristo.pl"+item for item in df['link']]

        # Convert 'price' column to float
        df['Price'] = pd.to_numeric(df['price'], errors='coerce')

        # Convert 'discount' column using pattern matching
        pattern = r"\d+"
        df['Discount'] = [int(re.search(pattern, disc).group()) if (isinstance(disc, str) and re.search(pattern, disc)) else 0 for disc in df['discount']]
        
        # Drop unnecessary columns 
        df.drop(['author_year', 'lang', 'cover', 'link', 'price', 'discount'], axis='columns', inplace=True)


        # Save the DataFrame to a CSV file without the index column
        df.to_csv('book_data.csv', index=False)

        

end = timer()
print(end - start)



