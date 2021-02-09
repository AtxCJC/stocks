import os
import json
from typing import Match
from bs4 import BeautifulSoup
import requests
import csv
from datetime import date
import pandas as pd

tickers = ['SQQQ', 'NOK', 'IDEX', 'AMD', 'BTCUSD']
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

    # name list
    exec(name+'=[]')

    # rating score
    score = soup.find('div', class_='gauge pull-right exampleDynamicGauge')
    score = score.attrs.get('data-value')
    print(score)
    exec(name+'.append(score)')

    # 90% chance between first and second
    first = soup.find_all('p', class_="text-justified")[1].find_all('strong')[1].text
    global second
    if first[0] != '$':
        first = soup.find_all('p', class_="text-justified")[1].find_all('strong')[2].text
        second = soup.find_all('p', class_="text-justified")[1].find_all('strong')[3].text
    else:
        second = soup.find_all('p', class_="text-justified")[1].find_all('strong')[2].text
    print(first, second)
    first = str(first)
    second = str(second)
    hold = first + " to " + second
    exec(name+'.append(hold)')

    # opening price
    try: 
        opening = soup.find('div', class_="col-lg-5 col-md-12").find('span', class_="text-danger bold").text
    except Exception as e:
        opening = soup.find('div', class_="col-lg-5 col-md-12").find('span', class_="text-success bold").text
    print(opening)
    exec(name+'.append(opening)')

    # RSI
    rsi = soup.find('small', class_="mb-0 mt-5").find('strong').text
    try:
        rsi = int(rsi)
    except ValueError:
        rsi = soup.find('small', class_="mb-0 mt-5").find_all('strong')[1].text
    print(rsi)
    exec(name+'.append(rsi)')


# dataframe
# today as the csv name
today = date.today()
today = str(today)
today += "_stocks.csv"
data = {'SQQQ':SQQQ, 'NOK':NOK, 'IDEX':IDEX, 'AMD':AMD, 'BTCUSD':BTCUSD}
types = ['Score', '3_Month_Hold', 'Opening_Price', 'RSI']
df = pd.DataFrame(data, index=types)
df.to_csv("../" + today)