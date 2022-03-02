import os
import pandas_datareader.tsp as tsp

import yfinance as yf

msft = yf.Ticker("VASGX")
#print(msft)
#print(msft.history(period='3mo'))

data = yf.download("MSFT", period = '1d', interval = '1h')
print(data)


#tspreader = tsp.TSPReader(start='2022-02-1', end='2022-02-19')
#print(tspreader.read())

