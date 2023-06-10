from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from timeit import default_timer as timer
import pandas as pd
import time

start = timer()

# Init:
gecko_path = '/mnt/c/Users/pearly/Desktop/WScrapping/geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

url = 'https://www.libristo.pl/books-in-english/humanities.html'

# creating empty dataframe
Title = [] 
Author = []  
Year = [] # Year of Published
CoverType = [] 
BookLink = []
Price = []
Disc = [] 

time.sleep(2)
driver.get(url)
time.sleep(2)

# Allow Cookies
button = driver.find_element(By.XPATH, '//button[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll" and @class="CybotCookiebotDialogBodyButton" and @tabindex="0"]')
button.click()
time.sleep(2)

LIMIT_PAGES = False

for page in range(1, 101):
    url = 'https://www.libristo.pl/books-in-english/humanities_' + str(page)+ '.html'
    driver.get(url)
    time.sleep(3)

    # Get Title
    titleElements = driver.find_elements(By.XPATH, "//li/div/h3/a")
    for titleElement in titleElements:
        try:
            titleElement = titleElement.text
        except:
            titleElement = '-'
        Title.append(titleElement)

    # Get Author & Year of Published
    # author & year of published are merged into one text
    # format : "author | publisher, year"
    authoryearElements = driver.find_elements(By.XPATH, "//li/div/h4")
    for authoryearElement in authoryearElements:
        elementtext = authoryearElement.text
        # strip the text to get author
        # get the first character
        try:
            if "|" in elementtext:
                authors = elementtext.split("|")[0]
            else:
                authors = "-"
        except:
            authors = '-'
        Author.append(authors)
        
        # strip the text to get years
        # get the last 4 characters
        try:
            years = elementtext[-4:]
        except:
            years = '-'
        Year.append(years)

    # Get Cover Type
    # format of the text : "Binding : soft/hard/etc"
    # so we need to strip again after ": " 
    covers = driver.find_elements(By.XPATH, "//p[strong[text()='Binding']]")
    for cover in covers:
        try:
            cover = cover.get_attribute("textContent")
            cover = cover.split(": ")[1]
        except:
            cover = '-'
        CoverType.append(cover)

    # Get BookLink
    links = driver.find_elements(By.XPATH, "//h3/a")
    for link in links:
        try:
            completelink = "https://www.libristo.pl"+link.get_attribute("href")
        except:
            completelink = '-'
        BookLink.append(completelink)

    # Get Price
    priceElements = driver.find_elements(By.XPATH, "//li/div[@class='LST_buy']/p/strong")
    for priceElement in priceElements:
        try:
            priceText = priceElement.text
        except:
            priceText ='-'
        Price.append(priceText)

    # Get Discount
    # text format : Sale xx %
    discElements = driver.find_elements(By.XPATH, "//li/div[@class='LST_buy']/div[1]")
    for discElement in discElements:
        try:
            discText = discElement.text
        except:
            discText = '-'
        Disc.append(discText)
        
driver.close()
end = timer()
print(end - start) # 767.7361544 = +/-12 mins

# ------------------------------ DATAFRAME ------------------------------
# tidying up what are scrapped to columns
df = pd.DataFrame({'Title': Title, 'Author': Author, 'Year':Year,'CoverType':CoverType,'BookLink':BookLink,'Price':Price,'Disc':Disc})

# Year : not every book written with published year
# if it is scrapped other than a 4 digits numeric value, then convert it to 0
df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0)

# Price : convert to float
df['Price'] = df['Price'].astype('float')

# Discount : not every book is sold with discount
# text format : Sale xx %
# if it is scrapped into "Buy" or "Pre-order" means no discount -> value = 0
# else : we get the value of discount
df['Disc'] = df['Disc'].apply(lambda x: 0 if x in ['Buy', 'Pre-order'] else int(x.split()[1])) # not every book has a discount. 

print(df)
df.to_csv("book.csv")
