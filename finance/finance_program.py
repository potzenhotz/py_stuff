#from yahoo_finance import Share
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime as dt

start = dt.datetime(2012,1,1)
end = dt.datetime.today()

stocks = ['AAPL', 'IBM', 'MSFT', 'GOOG', 'NTT.F']


all_data = {}
for ticker in stocks:
    all_data[ticker] = web.get_data_yahoo(ticker, start, end )
    
price = pd.DataFrame({tic: data['Adj Close']
                    for tic, data in all_data.items()})
                


n_stock_x = stocks
stock_x = 'AAPL'

price_norm =( (price[n_stock_x] 
              - price[n_stock_x].mean()) 
              / (price[n_stock_x].max() 
              - price[n_stock_x].min())
            )

#PLOTTTING
price[stock_x].plot()
plt.figure(1)


price_norm.plot()
plt.figure(2)

plt.show()
