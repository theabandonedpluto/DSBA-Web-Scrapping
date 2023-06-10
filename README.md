# How to run scrappers | quick guide 
## 1. Beautiful Soup 

## 2. Scrapy 
- download `libristo` scrapy project folder
- in `bookSpider.py` the `page_limit` is set to True and spider scraps 100 links: change the default in .__init__ constructor if the different number to be scrapped
- in bash, run command `scrapy crawl bookSpider`
- code will generate `book_data.csv` output

## 3. Selenium
