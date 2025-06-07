# Custom-Index-of-Stock-Market
User defined stock market custom index and visualized with time series chart and histogram
1. maav.py is the script to calculate custom index, save the data file, create time series chart and histogram chart based on end-of-day market close prices.
2. macnbc.py is the script to calculate customer index based on current market prices.
3. histodata_20250606.csv is an example of the data file created by maav.py.
4. ma_20250606.png is an example of the time series chart and histogram chart.
5. it is required to login in to alpha vantage to apply an app key.
6. it is also required to install all the python packages required.
7. run maav.py -d once a day after the market close for about one hour
8. if you need to run it second time, you can use the command maav.py -f histodata_yyyymmdd.csv.
9. run macnbc.py when market is open, and compare its value against the values of previous day. 
