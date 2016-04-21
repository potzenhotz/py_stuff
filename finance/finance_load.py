#!/usr/bin/env python
import pandas_datareader.data as web
import pandas as pd
import datetime as dt


def get_price(reload_data, ticker_list, start, end):
    f_loc = '/Users/Potzenhotz/python/finance/data/'
    f_title = 'stocks_data' + str(start) + '.csv'
    f_name = f_loc + f_title
    if reload_data:
        write_data = True
        read_data = False
    else:
        write_data = False
        read_data = True
    #-----------------------------------------------------------------------
    #Load Finance Data
    #-----------------------------------------------------------------------
    if reload_data:
        all_data = {}
        i=-1
        for ticker in ticker_list:
            i+=1
            print(i,ticker)
            try:
                all_data[ticker] = web.get_data_yahoo(ticker, start, end )
            except:
                print ("Cant find ", ticker)
                pass
        price = pd.DataFrame({tic: data['Adj Close']
                            for tic, data in all_data.items()})
         
    #-----------------------------------------------------------------------
    #Write Finance Data
    #-----------------------------------------------------------------------
    if write_data:
        price.to_csv(f_name)               
        #Reread data to get right format
        #while loading Date is index after reading Date will be column
        price = pd.read_csv(f_name)
    
    
    #-----------------------------------------------------------------------
    #Read Finance Data
    #-----------------------------------------------------------------------
    if read_data:
        #check if end date is current date
        if (end.date() != dt.datetime.today().date()):
            print('#####')
            print('Caution data is out of date: %s' % (end))
            print('#####')
        price = pd.read_csv(f_name)



    return price



