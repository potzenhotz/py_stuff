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

class MS_StatsExtract(object):
    """ 
        Using morning star ajax call.
        Can only get one stock at a time.
    """
    def __init__(self):
        """ List of url parameters -- for url formation """
        self.com_data_start_url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?&callback=?&t=XSES:'
        self.com_data_stock_portion_url = '' 
        self.com_data_stock_portion_additional_url = ''# for adding additonal str to the stock url.
        self.com_data_end_url = '&region=sgp&culture=en-US&cur=&order=asc'
        self.com_data_full_url = ''
        self.stock_list = ''#list of stock to parse. 

        ## printing options
        self.__print_url = 0

        ## temp csv storage path
        self.ms_stats_extract_temp_csv = 'ms_stats.csv'
        self.ms_stats_extract_temp_csv_transpose = 'ms_stats_t.csv'

        ## Temp Results storage
        self.target_stock_data_df = object() 
        
        ## full result storage
        self.com_data_allstock_df = pandas.DataFrame()
        self.hist_company_data_trends_df = pandas.DataFrame()



if __name__ == '__main__':
    #file = r'C:\data\compile_stockdata\full_20150719.csv'
    #full_stock_data_df = pandas.read_csv(file)
    #stock_list = list(full_stock_data_df['SYMBOL'])
    #stock_list = [n.strip('.SI') for n in stock_list]

    #stock_list = ['GILD', 'USE']
    #print ('Processing historical financial stats data')
    #pp = MS_StatsExtract()
    #pp.set_stocklist(stock_list)
    #pp.get_com_data_fr_all_stocks()


    csv_url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?t=FB'

    #print(cr)
    #df = pd.read_csv(csv_url, skiprows=2, names=["Sequence", "Start", "End", "Coverage", 'bla','bla','bla','bla','bla',])
    df = pd.read_csv(csv_url, skiprows=2, sep=',')

    df_part_1 = df.iloc[:15]

    df_part_1.to_csv('out.csv')
