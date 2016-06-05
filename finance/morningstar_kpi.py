"""
    Morning star finance stats scraping.
    Retrieve the information based on the export to csv button in morning star finance web page.

    Most parts used from spidezad:
    https://github.com/spidezad/MorningStar_stock_finance_stat_scraping/blob/master/MorningStar_stock_finance_stat_scraping.py
"""

#from __future__ import print_function
import csv
import requests
import pandas as pd
import sys
import os
import time
import matplotlib.pyplot as plt


class MS_StatsExtract(object):
    ''' 
        Using morning star ajax call.
        Can only get one stock at a time.
    '''
    def __init__(self, country, theme):
        ''' List of url parameters -- for url formation '''
        self.country = country
        self.theme = theme
        if self.country == 'us':
            self.start_url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?t='
        if self.country == 'ger':
            self.start_url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?t=XETR:'
        self.stock_portion_url = '' 
        self.end_url = ''
        self.full_url = ''
        self.stock_list = ''#list of stock to parse. 

        #Data Directories
        self.dir_raw_data = '/Users/Potzenhotz/Dropbox/stock_data/raw_data/'
        self.dir_data = '/Users/Potzenhotz/Dropbox/stock_data/data/'

        ''' printing options'''
        self.__print_debug = 0
        self.__print_info = 0
        self.__print_test = 0
        self.__print_processing = 1


        ## temp csv storage path
        self.ms_stats_extract_temp_csv = 'ms_stats.csv'
        self.ms_stats_extract_temp_csv_transpose = 'ms_stats_t.csv'


    def set_stocklist(self, stocklist):
       '''make the stock list property of object'''
       self.stock_list = stocklist

    def set_stock_url_portion(self,stock_sym):
        '''Define url portion for stock list'''
        self.stock_portion_url = stock_sym
   
    def merge_full_url(self):
        '''Combine start url with stock symbole'''
        self.full_url = self.start_url + self.stock_portion_url + self.end_url

    def write_df(self,df,fname):
        '''Write dataframe to csv'''
        if self.__print_info: print ('Info: Entering write_df')

        df.to_csv(fname)

    def read_df(self,fname):
        '''Read dataframe from csv file'''
        if self.__print_info: print ('Info: Entering read_df')

        self.read_df = pd.read_csv(fname, index_col=0)

    def read_stock_list(self, stock_fname, delimiter):
        self.stock_fname = stock_fname
        raw_ticker_list = pd.read_csv(stock_fname, sep=delimiter, encoding='cp1252') 
        #some kind of windows encoding cp1252. Excel is creating it...
        ticker_list = pd.DataFrame(raw_ticker_list)
        if self.__print_info: print(ticker_list.Symbol)
        if self.__print_info: print(raw_ticker_list.index.values)
        if self.country == 'ger':
            ticker_list.Symbol.replace(regex=True,inplace=True,to_replace=r'.DE',value=r'')
        self.stock_list= ticker_list.Symbol
        self.set_stocklist(self.stock_list)
 
    
    def read_raw_df(self):
        '''Read dataframe from csv file'''
        if self.__print_info: print ('Info: Entering read_RAW_df')

        fname = (self.dir_raw_data + 'raw_df_' + str(self.stock_portion_url) + '.csv')
        if self.__print_debug: print ('Debug: in read_raw_df')
        if self.__print_debug: print ('Debug:', fname)
        self.raw_df = pd.read_csv(fname, index_col = 0)
        if self.__print_test: print ('Test:', self.raw_df)

    def check_data_exist(self):
        '''Check if data file already exists'''
        if self.__print_info: print ('Info: Entering check_data_exist')

        fname = (self.dir_raw_data + 'raw_df_'  + str(self.stock_portion_url) + '.csv')
        self.data_exist = os.path.isfile(fname) 
        if self.__print_debug: print ('Debug: File existance of', self.stock_portion_url,'is:', self.data_exist)
        '''Check if file older than 3 month'''
        if self.data_exist == True:
            self.file_older_3_month = time.time() - os.path.getmtime(fname) > (6 * 24 * 60 * 60)
            if self.file_older_3_month == True:
                self.data_exist = False
            if self.__print_debug: print ('Debug: File age in h:', (time.time() - os.path.getmtime(fname))/60/60/24)

    def download_data(self):
        '''Download the data using panda'''
        if self.__print_info: print ('Info: Entering download_data')

        self.download_fault = 0
        self.no_data = False
        self.data_exist = False
        self.check_data_exist()
        if self.data_exist == False:
            try:
                if self.__print_debug: print ('Debug: Download raw df')
                self.raw_df = pd.read_csv(self.full_url, skiprows=2, sep=',')
                self.raw_df = self.raw_df.rename(columns={'Unnamed: 0': 'KPI_General'})

                fname = self.dir_raw_data + 'raw_df_' + str(self.stock_portion_url) + '.csv'
                self.write_df(self.raw_df,fname)
            except:
                if self.__print_debug: print('Problem with processing this data: ', self.full_url)
                self.no_data = True
                print('Prblem with stock: ', self.stock)
                e_1 = sys.exc_info()[0]
                e_2 = sys.exc_info()[1]
                print( "Error: %s with %s" % (e_1, e_2) )
        else:
            self.read_raw_df()

    def load_stock_data(self):
        '''
        1) Combine stock url
        2) Load Data
        '''
        if self.__print_info: print ('Info: Entering load_stock_data')

        self.merge_full_url()
        if self.__print_debug: print ('Debug:',self.full_url)
        self.download_data()

    def restructure_stock_data(self):
        '''Split the raw datafile into:
            1) General
            2) Profitability
            3) Growth
            4) Revenue
            5) Operating Income
            6) Net Income
            7) EPS
            8) Cash Flow
            9) Financial Health
            10) Liquidity Financial Health
            11) Efficieny 
        '''
        if self.__print_info: print ('Info: Entering restructure_stock_data')

        self.raw_df = self.raw_df.replace(',','', regex = True)
        self.raw_df = self.raw_df.set_index('KPI_General')

        self.df_part_1 = self.raw_df.iloc[:15]

        self.df_part_2 = self.raw_df.iloc[17:25]
        self.df_part_2 = self.df_part_2.rename(columns={'KPI_General': 'KPI_Profitability'})

        self.df_part_3 = self.raw_df.iloc[27:34]
        self.df_part_3 = self.df_part_3.rename(columns={'KPI_General': 'KPI_Growth'})

        self.df_part_4 = self.raw_df.iloc[38:42]
        self.df_part_4 = self.df_part_4.rename(columns={'KPI_General': 'KPI_Revenue_%'})

        self.df_part_5 = self.raw_df.iloc[43:47]
        self.df_part_5 = self.df_part_5.rename(columns={'KPI_General': 'KPI_Operating_Income_%'})

        self.df_part_6 = self.raw_df.iloc[48:52]
        self.df_part_6 = self.df_part_5.rename(columns={'KPI_General': 'KPI_Net_Income_%'})

        self.df_part_7 = self.raw_df.iloc[53:57]
        self.df_part_7 = self.df_part_7.rename(columns={'KPI_General': 'EPS_%'})

        self.df_part_8 = self.raw_df.iloc[59:64]
        self.df_part_8 = self.df_part_8.rename(columns={'KPI_General': 'KPI_Cash_Flow'})

        self.df_part_9 = self.raw_df.iloc[66:86]
        self.df_part_9 = self.df_part_9.rename(columns={'KPI_General': 'KPI_Financial_Health'})

        self.df_part_10 = self.raw_df.iloc[87:91]
        self.df_part_10 = self.df_part_10.rename(columns={'KPI_General': 'KPI_Liquidity_Financial_Health'})

        self.df_part_11 = self.raw_df.iloc[93:101]
        self.df_part_11 = self.df_part_11.rename(columns={'KPI_General': 'KPI_Efficiency'})


        self.frames = [self.df_part_1, self.df_part_2, self.df_part_3, self.df_part_4 
                , self.df_part_5 , self.df_part_6, self.df_part_7, self.df_part_8  
                , self.df_part_9, self.df_part_10, self.df_part_11]

        self.df_full = pd.concat(self.frames)
        if self.__print_test: print(self.df_full)


    def plot_data(self,df):
        '''Plot some KPIs'''
        if self.__print_info: print ('Info: Entering plot_data')
        #df = df.transpose()
        df = df.astype(float)

        EPS = df.iloc[5]
        EPS.plot(title=str(self.stock_portion_url), legend = True)

        Dividends = df.iloc[6]
        Dividends.plot(title=str(self.stock_portion_url), legend = True)

        Book_value = df.iloc[9]
        Book_value.plot(title=str(self.stock_portion_url), legend = True)

        fname = 'KPI_General_plot_' + str(self.stock_portion_url) 
        plt.savefig(fname)
        plt.close()

    def get_data_for_all_stocks(self):
        '''All steps to get the data'''
        if self.__print_info: print ('Info: Entering get_data_for_all_stocks')

        self.counter_extract = 0
        for self.stock in self.stock_list:
            try:
                if self.__print_processing: print('Processing stock:', self.stock)
                self.set_stock_url_portion(self.stock)
                self.load_stock_data()
                if self.no_data == False:
                    self.restructure_stock_data()
                    self.extract_important_kpis()
                    self.counter_extract += 1
            except:
                print('Prblem with stock: ', self.stock)
                e_1 = sys.exc_info()[0]
                e_2 = sys.exc_info()[1]
                print( "Error: %s with %s" % (e_1, e_2) )


    def extract_important_kpis(self):
        if self.__print_info: print ('Info: Entering extract_important_kpis')
        
        if self.counter_extract == 0:
            #create files
            self.fname_kpi_collection = self.dir_data + theme + '_'+'kpi_collection.csv'
            f = open(self.fname_kpi_collection, 'w')
            writer = csv.writer(f)
            writer.writerow( ('Symbol', 'EPS', 'Dividends', 'Book_value') )
            f.close()

        EPS = self.df_full.iloc[5]
        Dividends = self.df_full.iloc[6]
        Book_value = self.df_full.iloc[9]

        
        f = open(self.fname_kpi_collection, 'a', newline='')
        writer = csv.writer(f)
        writer.writerow( (self.stock, EPS.TTM, Dividends.TTM, Book_value.TTM) )
        f.close()
       

    def analyze_important_kpis(self):
        if self.__print_info: print ('Info: Entering analyze_important_kpis')

        self.fname_kpi_collection = self.dir_data + theme + '_' +'kpi_collection.csv'
        self.read_df(self.fname_kpi_collection)
        self.analyze_important_kpis = self.read_df
        print (self.analyze_important_kpis.head())

        raw_sorted_EPS = self.analyze_important_kpis.EPS.sort_values(ascending=False)
        raw_sorted_Dividends = self.analyze_important_kpis.Dividends.sort_values(ascending=False)
        raw_sorted_Book_value = self.analyze_important_kpis.Book_value.sort_values(ascending=False)

        top_10_EPS = raw_sorted_EPS[:10] #:10 takes first 10 values of array
        top_10_Dividends = raw_sorted_Dividends[:10] #:10 takes first 10 values of array
        top_10_Book_value = raw_sorted_Book_value[:10] #:10 takes first 10 values of array


if __name__ == '__main__':
    '''
    If python program is not called inside another python program
    '''
    which_stock_list = 'Test_us'
    #which_stock_list = 'Test_ger'
    #which_stock_list = 'DAX'
    #which_stock_list = 'MDAX'
    #which_stock_list = 'SDAX'
    #which_stock_list = 'TECDAX'
    #which_stock_list = 'NDX100'
    which_stock_list = 'SP500'
    


    if which_stock_list == 'Test_us':
        country='us' 
        theme = 'TEST_US'
        us_stock_list = ['AMZ', 'GILD' ]
        #us_stock_list = ['GILD' ]
        stocks = MS_StatsExtract(country, theme)
        stocks.set_stocklist(us_stock_list)
        stocks.get_data_for_all_stocks()
        stocks.analyze_important_kpis()

    if which_stock_list == 'Test_ger':
        country='ger' 
        theme = 'TEST_GER'
        ger_stock_list = ['DAI', 'BAYN', 'AIR']
        stocks = MS_StatsExtract(country, theme)
        stocks.set_stocklist(ger_stock_list)
        stocks.get_data_for_all_stocks()
        stocks.analyze_important_kpis()

    if which_stock_list == 'MDAX':
        fname = '/Users/Potzenhotz/Dropbox/stock_data/MDAX.csv'
        delimiter = ';'
        country = 'ger' 
        theme = 'MDAX'
        stocks = MS_StatsExtract(country, theme)
        stocks.read_stock_list(fname, delimiter)
        stocks.get_data_for_all_stocks()
        stocks.analyze_important_kpis()



    if which_stock_list == 'SP500':
        fname = '/Users/Potzenhotz/Dropbox/stock_data/' + which_stock_list +'.csv'
        delimiter = ';'
        country = 'us' 
        theme = 'SP500'
        stocks = MS_StatsExtract(country, theme)
        stocks.read_stock_list(fname, delimiter)
        #stocks.get_data_for_all_stocks()
        stocks.analyze_important_kpis()






