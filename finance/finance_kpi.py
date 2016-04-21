#!/usr/bin/env python

import pandas as pd
import datetime as dt
import yahoo_finance as yf

stocks_name = 'YHOO'
yahoo = yf.Share(stocks_name)
stocks_obj = yahoo
info = {'info' : stocks_obj.get_info()}
columns = [
  'avg_daily_volume'
, 'stock_exchange' 
, 'market_cap' 
, 'book_value' 
, 'ebitda' 
, 'dividend_share' 
, 'dividend_yield' 
, 'earnings_share' 
, 'year_high' 
, 'year_low' 
, '50day_moving_avg' 
, '200day_moving_avg' 
, 'price_earnings_ratio' 
, 'earnings_growth_ratio' 
, 'price_sales' 
, 'price_boom' 
, 'short_ratio' 
]
all_data = [(
 stocks_obj.get_avg_daily_volume()
, stocks_obj.get_stock_exchange()
, stocks_obj.get_market_cap()
, stocks_obj.get_book_value()
, stocks_obj.get_ebitda()
, stocks_obj.get_dividend_share()
, stocks_obj.get_dividend_yield()
, stocks_obj.get_earnings_share()
, stocks_obj.get_year_high()
, stocks_obj.get_year_low()
, stocks_obj.get_50day_moving_avg()
, stocks_obj.get_200day_moving_avg()
, stocks_obj.get_price_earnings_ratio()
, stocks_obj.get_price_earnings_growth_ratio()
, stocks_obj.get_price_sales()
, stocks_obj.get_price_book()
, stocks_obj.get_short_ratio()
)]
#        for ticker in ticker_list:
#            i+=1
#            print(i,ticker)
#            try:
#                all_data[ticker] = web.get_data_yahoo(ticker, start, end )
#            except:
#                print ("Cant find ", ticker)
#                pass
#        price = pd.DataFrame({tic: data['Adj Close']
#                            for tic, data in all_data.items()})
# 
kpi_df = pd.DataFrame(all_data, index=[stocks_name], columns=columns) 
print(kpi_df)
