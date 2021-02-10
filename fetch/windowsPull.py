import os
import json
from typing import Match
from bs4 import BeautifulSoup
import requests
import csv
from datetime import date
import pandas as pd
import time
from datetime import datetime, timedelta

tickers = ['SQQQ', 'NOK', 'IDEX', 'AMD', 'BTCUSD', 'FBIO', 'SONM']
ticker = list(tickers)

# puts list of tickers into folder as html request
# for name in tickers:
#     get = "wget -O ../tickers/"
#     url = " https://stockinvest.us/stock/"
#     get = get + name + '.html'
#     url = url + name
#     getURL = get + url
#     print(getURL)
#     os.system(getURL)
#     time.sleep(1)

# last = date.today() - timedelta(days=1)
last = '2021-02-08'
last = str(last)
last = "../outputs/" + last + "_stocks.csv"
df_past = pd.read_csv(last)
past = []

# for name in tickers:
#     try:
#         print(df_past.iloc[0][name])
#         past.append(df_past.iloc[0][name])
#     except KeyError:
#         print("NA")
#         past.append("NA")
# print(past)

for name in tickers:
    location = '../tickers/'
    location = location + name + '.html'
    print("\n", location)
    with open(location) as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    # name list
    exec(name+'=[]')

    try:
        past = (df_past.iloc[0][name])
    except KeyError:
        past = "NA"

    # rating score
    score = soup.find('div', class_='gauge pull-right exampleDynamicGauge')
    score = score.attrs.get('data-value')
    print(score)
    exec(name+'.append(score)')

    
    # dif
    try:
        score, past = float(score), float(past)
        if float(score) > float(past) and past != 'NA':
            print(score, ">", past)
            dif = score - past
            dif = str(abs((round(dif, 2))))
            dif = "UP+ " + dif
            print(dif)
            exec(name+'.append(dif)')
        elif float(score) < float(past) and past != 'NA':
            print(score, "<", past)
            dif = past - score
            dif = str(abs((round(dif, 2))))
            dif = "DOWN- " + dif
            print(dif)
            exec(name+'.append(dif)')
    except ValueError:
        score, dif = float(score), str(score)
        dif = "SAME " + dif
        print(dif)
        exec(name+'.append(dif)')
    
    
    

    # 90% chance between first and second
    first = soup.find_all('p', class_="text-justified")[1].find_all('strong')[1].text
    global second
    if first[0] != '$':
        first = soup.find_all('p', class_="text-justified")[1].find_all('strong')[2].text
        second = soup.find_all('p', class_="text-justified")[1].find_all('strong')[3].text
    else:
        try:
            second = soup.find_all('p', class_="text-justified")[1].find_all('strong')[2].text
        except IndexError as e:
            first, second = "NA", ""
    print(first, second)
    first = str(first)
    second = str(second)
    hold = first + " - " + second
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

    # append past
    try:
        past = (df_past.iloc[0][name])
        print(past)
        exec(name+'.append(past)')
    except KeyError:
        past = "NA"
        print(past)
        exec(name+'.append(past)')


# dataframe
# today as the csv name
# today = date.today()
today = '2021-02-09'
today = str(today)
today += "_stocks.csv"
types = ['Score', 'Score_Dif', '3_Month_Hold', 'Opening_Price', 'RSI', 'Day_1']
data = {'SQQQ':SQQQ, 'NOK':NOK, 'IDEX':IDEX, 'AMD':AMD, 'BTCUSD':BTCUSD, 'FBIO':FBIO, 'SONM':SONM}
df = pd.DataFrame(data, index=types)
df.to_csv("../outputs/" + today)