'''
    -Load data-
    Yahoo finance stock scraping.
    Retrieve the information based on the export to csv button in yahoo finance web page.
'''
import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import os
import time

class StockExtract(object):
    ''' 
        Load stock data from yahooo.
        Can only get one stock at a time.
    '''
    

    def __init__(self):
        ''' List of url parameters -- for url formation '''
        self.floc = '/Users/Potzenhotz/python/finance/data/'
        self.ftitle = ''

        ''' printing options'''
        self.__print_debug = 1
        self.__print_info = 1

    def set_dates(self,year):
        self.start_date = dt.datetime(year,1,1).date()
        self.end_date = dt.datetime.today()

    def set_filename(self, fname):
        self.ftitle = fanme + '_' + str(self.start_date) + '.csv'
        self.fname = self.floc + self.ftitle

    def set_stocklist(self, stocklist):
       '''make the stock list property of object'''
       self.stock_list = stocklist

    def check_data_exist(self):
        '''Check if data file already exists'''
        self.data_exist = os.path.isfile(self.fname) 
        '''Check if file older than 3 month'''
        if self.data_exist == True:
            self.file_older_3_month = time.time() - os.path.getmtime(self.fname) > (3 * 30 * 24 * 60 * 60)
            if self.file_older_3_month == True:
                self.data_exist = False
            if self.__print_debug: print ('Debug: File age in h:', (time.time() - os.path.getmtime(self.fname))/60/60/24)

    def write_raw_df(self):
        '''Write dataframe to csv'''
        self.raw_df.to_csv(self.fname)

    def read_raw_df(self):
        '''Read dataframe from csv file'''
        if self.__print_debug: print ('Debug: in read_raw_df')
        if self.__print_debug: print ('Debug:', self.fname)
        self.raw_df = pd.read_csv(self.fname, index_col = 0)

    def load_data(self):
        '''Download the data using panda'''
        self.data_exist = False
        self.check_data_exist()
        self.all_data = {}
        if self.data_exist == False:
            i=-1
            for ticker in self.stock_list:
                i+=1
                if self.__print_info: print ('Info: ',i, ticker)
                try:
                    self.all_data[ticker] = web.get_data_yahoo(ticker, self.start_date, self.end_date )
                except:
                    if self.__print_info: print('Cant find: ', ticker)
                    pass
            self.raw_df = pd.DataFrame({tic: data['Adj Close'] for tic, data in self.all_data.items()})
            self.write_raw_df()
        else:
            self.read_raw_df()

        




if __name__ == '__main__':
    '''
    If python program is not called inside another python program
    '''
    fname = 'my_list'
    stock_fname = '/Users/Potzenhotz/Documents/stock_data/stock_estimations.csv'
    year=2015
    
    #stock_list = ['GILD', 'GOOG' ]

    stocks = StockExtract()

    #stocks.set_stocklist(stock_list)

    stocks.set_dates(year)
    stocks.set_filename(fname)
    stocks.read_stock_list(stock_fname)
    stocks.load_data()


