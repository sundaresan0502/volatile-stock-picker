import os
import requests
import collections
import csv
from dotenv import load_dotenv

# load all data .env file
load_dotenv()

urlStr = "https://finnhub.io/api/v1/quote?symbol={}&token={}"     
# get the api key from the .env file     
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')          
stocks_Code = ['AAPL', 'AMZN', 'NFLX', 'META', 'GOOGL']
# create dictionary map to hold the stock details
stocks_Data = collections.OrderedDict()
stocks_Volatile_Data = collections.OrderedDict()

for current_Stock_Code in stocks_Code:
    # by running this loop, we are sending request to finnhub and collect the stocks Data
    url = urlStr.format(current_Stock_Code, FINNHUB_API_KEY)
    data = requests.get(url)
    stockData = data.json()
    # store the stock details into dict map with stockCode as 'key' and details as a 'value'
    stocks_Data[current_Stock_Code] = stockData
    currentPrice = stockData['c']
    previous_Close_Price = stockData['pc']
    # calculate the volatile percentage for particular stock
    differencePercentage = (((currentPrice - previous_Close_Price) / ((currentPrice + previous_Close_Price)/2)) * 100)
    current_Volatile = round(differencePercentage, 2)
    # store volatile details into map with stockCode as 'key' and volatile percentage as a 'value'
    stocks_Volatile_Data[current_Stock_Code] = abs(current_Volatile)

# get the most volatile stock from our volatileData map
most_Volatile_Stock = max(stocks_Volatile_Data, key= lambda x: stocks_Volatile_Data[x])
most_Volatile_Stock_Data = stocks_Data.get(most_Volatile_Stock)

# create list with corresponding name and data to crate and store the data into CSV
header = ['stock_symbol', 'percentage_change', 'current_price', 'last_close_price']
data = [most_Volatile_Stock, stocks_Volatile_Data.get(most_Volatile_Stock), most_Volatile_Stock_Data['c'], most_Volatile_Stock_Data['pc']]

with open('most_volatile_stock.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerow(data)

print("Hi There!, Most Volatile Stock Details are written in most_volatile_stock.csv, please check that file")