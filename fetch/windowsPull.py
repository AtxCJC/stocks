import os
import json
from typing import Match
from bs4 import BeautifulSoup
import requests
import csv
from datetime import date
import pandas as pd

tickers = ['SQQQ', 'NOK', 'IDEX', 'AMD']
ticker = list(tickers)

# puts list of tickers into folder as html request
for name in tickers:
    get = "wget -O ../tickers/"
    url = " https://stockinvest.us/stock/"
    get = get + name + '.html'
    url = url + name
    getURL = get + url
    print(getURL)
    os.system(getURL)


for name in tickers:
    location = '../tickers/'
    location = location + name + '.html'
    print("\n", location)
    with open(location) as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    # today as the csv name
    today = date.today()
    today = str(today)
    today += "_stocks.csv"
    # open csv to write
    with open("../" + today, mode='w') as my_csv:
        wr = csv.writer(my_csv, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        wr.writerow(tickers)

    # rating score
    score = soup.find('div', class_='gauge pull-right exampleDynamicGauge')
    score = score.attrs.get('data-value')
    print(score)

    # 90% chance between first and second
    first = soup.find_all('p', class_="text-justified")[1].find_all('strong')[1].text
    global second
    if first[0] != '$':
        first = soup.find_all('p', class_="text-justified")[1].find_all('strong')[2].text
        second = soup.find_all('p', class_="text-justified")[1].find_all('strong')[3].text
    else:
        second = soup.find_all('p', class_="text-justified")[1].find_all('strong')[2].text
    print(first, second)

    # opening price
    try: 
        opening = soup.find('div', class_="col-lg-5 col-md-12").find('span', class_="text-danger bold").text
    except Exception as e:
        opening = soup.find('div', class_="col-lg-5 col-md-12").find('span', class_="text-success bold").text
    print(opening)

    # RSI
    rsi = soup.find('small', class_="mb-0 mt-5").find('strong').text
    try:
        rsi = int(rsi)
    except ValueError:
        rsi = soup.find('small', class_="mb-0 mt-5").find_all('strong')[1].text
    print(rsi)


