import requests
import csv
from bs4 import BeautifulSoup

"""This is a simple Web-Scrapping program that I built for collecting inspirational quotes from www.passiton.com,
and saving them to a CSV file. For this task I have used the following libraries:

- Requests --> To make HTTP requests to access the website
- html5lib --> To parse HTML content from the website, and handle HTML5-specific parsing that can used by Bs4.
- BeautifulSoup --> To parse HTML content from the website, and pull the values that will be added to the CSV file.
"""

URL = "https://www.passiton.com/inspirational-quotes"
r = requests.get(URL)
# print(r.content)

soup = BeautifulSoup(r.content, 'html5lib')

with open('prettify.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
    
print("prettify.html created")

quotes = []

table = soup.find('div', attrs={'id':'all_items'})

for i in table.find_all('div', attrs={'class':"text-center mb-8"}):
    quote={}
    quote['theme'] = i.h5.text
    quote['url'] = i.a['href']
    quote['img'] = i.img['src']
    quote['lines'] = i.img['alt'].split(" #")[0]
    quote['author'] = i.find('p', class_= 'text-white/50').get_text(strip=True)
    quotes.append(quote)
    

filename = 'web_scraped.csv'
with open(filename, 'w', newline='') as file:
    w = csv.DictWriter(file, ['theme', 'url', 'img', 'lines', 'author'])
    w.writeheader()
    for quote in quotes:
        w.writerow(quote)
        
print("Successfully extracted the data into CSV File.")