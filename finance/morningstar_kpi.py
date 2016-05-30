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
    def __init__(self, country):
        ''' List of url parameters -- for url formation '''
        if country == 'us':
            self.start_url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?t='
        if country == 'ger':
            self.start_url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?t=XETR:'
        self.stock_portion_url = '' 
        self.end_url = ''
        self.full_url = ''
        self.stock_list = ''#list of stock to parse. 

        ''' printing options'''
        self.__print_debug = 1


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

    def write_raw_df(self):
        '''Write dataframe to csv'''
        fname = 'raw_df_' + str(self.stock_portion_url) + '.csv'
        self.raw_df.to_csv(fname)

    def read_raw_df(self):
        '''Read dataframe from csv file'''
        fname = ('raw_df_' + str(self.stock_portion_url) + '.csv')
        if self.__print_debug: print ('Debug: in read_raw_df')
        if self.__print_debug: print ('Debug:', fname)
        self.raw_df = pd.read_csv(fname, index_col = 0)

    def check_data_exist(self):
        '''Check if data file already exists'''
        fname = ('raw_df_' + str(self.stock_portion_url) + '.csv')
        self.data_exist = os.path.isfile(fname) 
        if self.__print_debug: print ('Debug: File existance of', self.stock_portion_url,'is:', self.data_exist)
        '''Check if file older than 3 month'''
        if self.data_exist == True:
            self.file_older_3_month = time.time() - os.path.getmtime(fname) > (3 * 30 * 24 * 60 * 60)
            if self.file_older_3_month == True:
                self.data_exist = False
            if self.__print_debug: print ('Debug: File age in h:', (time.time() - os.path.getmtime(fname))/60/60/24)

    def download_data(self):
        '''Download the data using panda'''
        self.download_fault = 0
        self.data_exist = False
        self.check_data_exist()
        if self.data_exist == False:
            try:
                if self.__print_debug: print ('Debug: Download raw df')
                self.raw_df = pd.read_csv(self.full_url, skiprows=2, sep=',')
                self.raw_df = self.raw_df.rename(columns={'Unnamed: 0': 'KPI_General'})
                self.write_raw_df()
            except:
                if self.__print_download_fault: print('Problem with processing this data: ', self.full_url)
                self.download_fault =1
        else:
            self.read_raw_df()

    def load_stock_data(self):
        '''
        1) Combine stock url
        2) Load Data
        '''
        self.merge_full_url()
        if self.__print_debug: print ('Debug:',self.full_url)
        self.download_data()

    def split_stock_data(self):
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


    def plot_data(self,df):
        '''Plot some KPIs'''
        #df = df.transpose()
        df = df.astype(float)
        ''' plot all of it
        for index, row in df.iterrows():
            row.plot(title ='test', legend=True)
            #row = data2.iloc[i]
        '''
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
        for stock in self.stock_list:
            try:
                print('Processing stock:', stock)
                self.set_stock_url_portion(stock)
                self.load_stock_data()
                self.split_stock_data()
                self.plot_data(self.df_part_1)
            except:
                print('Prblem with stock: ', stock)
                e_1 = sys.exc_info()[0]
                e_2 = sys.exc_info()[1]
                print( "Error: %s with %s" % (e_1, e_2) )



if __name__ == '__main__':
    '''
    download = True
    download = False
    if download == True:
        csv_url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?t=GILD'
        #csv_url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?t=FB'

        df = pd.read_csv(csv_url, skiprows=2, sep=',' )
        df = df.rename(columns={'Unnamed: 0': 'KPI_General'})

        df.to_json('kpi_json')
        df.to_csv('kpi_csv')
    else:
        df = pd.read_csv('kpi_csv', index_col=0)





    lst_dfs = [df[66:],df_part_1, df_part_2, df_part_3, df_part_4, df_part_5, df_part_6, df_part_7, df_part_8, df_part_9]
    test_print=True
    if test_print == True:
        for df_part in lst_dfs: 
            print(df_part)
            print('##########################')
            print(df_part.index)
            print(df_part.columns)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    '''
    country='us' 
    us_stock_list = ['GILD', 'GOOG' ]
    #stock_list = ['BAYN']
    stocks = MS_StatsExtract(country)
    stocks.set_stocklist(us_stock_list)
    stocks.get_data_for_all_stocks()

    country='ger' 
    ger_stock_list = ['BAYN','DAI' ]
    stocks = MS_StatsExtract(country)
    stocks.set_stocklist(ger_stock_list)
    stocks.get_data_for_all_stocks()


