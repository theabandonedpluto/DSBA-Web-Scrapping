
import pandas as pd

links = pd.DataFrame(columns=['url'])
links.loc[0, 'url'] = 'https://www.libristo.pl/books-in-english/humanities'

for page in range(2, 101):
    url = 'https://www.libristo.pl/books-in-english/humanities_' + str(page)+ '.html'
    links.loc[page-1, 'url'] = url

print(links)
links.to_csv('links.csv', index=False)
