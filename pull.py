import os
import json
from typing import Match
from bs4 import BeautifulSoup
import requests

tickers = {'SQQQ', 'NOK', 'IDEX', 'AMD'}

# puts list of tickers into folder as html request
# for name in tickers:
#     get = "wget -O ./tickers/"
#     url = " https://stockinvest.us/stock/"
#     get = get + name + '.html'
#     url = url + name
#     getURL = get + url
#     print(getURL)
#     os.system(getURL)

# reading 90% chance between
for name in tickers:
    location = './tickers/'
    location = location + name + '.html'
    print(location)
    with open(location) as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    # rating score
    score = soup.find('div', class_='gauge pull-right exampleDynamicGauge')
    score = score.attrs.get('data-value')
    print(score)

    first = soup.find_all('p', class_="text-justified")[1].find_all('strong')[1].text
    global second
    if first[0] != '$':
        first = soup.find_all('p', class_="text-justified")[1].find_all('strong')[2].text
        second = soup.find_all('p', class_="text-justified")[1].find_all('strong')[3].text
    else:
        second = soup.find_all('p', class_="text-justified")[1].find_all('strong')[2].text
    print(first, second)

