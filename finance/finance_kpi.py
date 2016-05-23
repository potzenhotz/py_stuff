#!/usr/bin/env python

import pandas as pd
import datetime as dt
import yahoo_finance as yf

stocks_name = 'GILD'
yahoo = yf.Share(stocks_name)
def stocks_kpi(stock_vector):
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

    kpi_df = pd.DataFrame(columns=columns) 


    for stocks_name in stock_vector:
        stocks_obj = yf.Share(stocks_name)
        info = {'info' : stocks_obj.get_info()}
        
        all_data = [
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
        ]
        kpi_df.loc[stocks_name] = all_data

    return kpi_df
test = ['GOOG','GLID', 'IBB', 'AMZN']

tests = stocks_kpi(test)
