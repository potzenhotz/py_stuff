
import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import finance_load as fl

par_reload_data = True
raw_ticker_list  = pd.read_csv('/Users/Potzenhotz/python/finance/nasdaqlisted.csv',delimiter='|')
ticker_list = pd.DataFrame(raw_ticker_list)

start_2015 = dt.datetime(2015,1,1).date()
end = dt.datetime.today()

price_nasdaq_2015 = fl.get_price(par_reload_data, ticker_list.Symbol, start_2015, end)



print (price_nasdaq_2015.head())
