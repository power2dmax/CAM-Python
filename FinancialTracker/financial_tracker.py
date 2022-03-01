import os
import pandas_datareader.tsp as tsp

# Request data via Yahoo public API
tspreader = tsp.TSPReader(start='2022-02-1', end='2022-02-19')

print(tspreader.read())

# Display Info

