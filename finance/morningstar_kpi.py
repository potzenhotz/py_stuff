"""
    Morning star finance stats scraping.
    Retrieve the information based on the export to csv button in morning star finance web page.

    partly used from spidezad:
    https://github.com/spidezad/MorningStar_stock_finance_stat_scraping/blob/master/MorningStar_stock_finance_stat_scraping.py
"""

#from __future__ import print_function
import csv
import requests
import pandas as pd
import pandas_datareader.data as web
import sys
import os
import time
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.relativedelta import relativedelta


class MS_StatsExtract(object):
    ''' 
        Using morning star ajax call.
        Can only get one stock at a time.
    '''
    def __init__(self, country, theme):
        ''' List of url parameters -- for url formation '''
        self.country = country
        self.theme = theme
        if self.country == 'us' or self.country == 'uk':
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
        self.__print_debug = 1
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
        '''
        reads stock list using csv format
        ->stock_fname needs to provide location if file is not in the same folder
        '''
        self.stock_fname = stock_fname
        raw_ticker_list = pd.read_csv(stock_fname, sep=delimiter, encoding='cp1252') 
        #some kind of windows encoding cp1252. Excel is creating it...
        ticker_list = pd.DataFrame(raw_ticker_list)
        if self.__print_info: print(ticker_list.Symbol)
        if self.__print_info: print(raw_ticker_list.index.values)
        if self.country == 'ger':
            ticker_list.Symbol.replace(regex=True,inplace=True,to_replace=r'.DE',value=r'')
        elif self.country == 'uk':
            ticker_list.Symbol.replace(regex=True,inplace=True,to_replace=r'.L',value=r'')
        self.stock_list= ticker_list.Symbol
        self.set_stocklist(self.stock_list)
 
    
    def read_raw_df(self):
        '''
        Read dataframe from csv file
        -> TO DO: only use read_df funcktion
        here: still hardcoded path
        '''
        if self.__print_info: print ('Info: Entering read_RAW_df')

        fname = (self.dir_raw_data + 'raw_df_' + str(self.stock_portion_url) + '.csv')
        if self.__print_info: print ('Info: in read_raw_df')
        if self.__print_info: print ('Info:', fname)
        self.raw_df = pd.read_csv(fname, index_col = 0)
        if self.__print_test: print ('Test:', self.raw_df)


    def check_data_exist(self):
        '''
        Check if data file already exists
        -TO DO: still with hardcoded path
        '''
        if self.__print_info: print ('Info: Entering check_data_exist')

        fname = (self.dir_raw_data + 'raw_df_'  + str(self.stock_portion_url) + '.csv')
        self.data_exist = os.path.isfile(fname) 
        if self.__print_info: print ('Info: File existance of', self.stock_portion_url,'is:', self.data_exist)
        '''Check if file older than 3 month'''
        if self.data_exist == True:
            self.check_age_of_file()
            #self.file_older_3_month = time.time() - os.path.getmtime(fname) > (6 * 24 * 60 * 60)
            #if self.file_older_3_month == True:
            #    self.data_exist = False
            #if self.__print_info: print ('Info: File age in h:', (time.time() - os.path.getmtime(fname))/60/60/24)

    def check_age_of_file(self):
        '''
        checks age of file and compares it to certain age
        -TO DO: still hardcoded file age comparison
        '''
        self.file_older_3_month = time.time() - os.path.getmtime(fname) > (6 * 24 * 60 * 60)
        if self.file_older_3_month == True:
            self.data_exist = False
        if self.__print_info: print ('Info: File age in h:', (time.time() - os.path.getmtime(fname))/60/60/24)

    def download_data(self):
        '''
        Download the data using panda
        -uses read_csv to download morningstar data
        '''
        if self.__print_info: print ('Info: Entering download_data')

        self.download_fault = 0
        self.no_data = False
        self.data_exist = False
        self.check_data_exist()
        if self.data_exist == False:
            try:
                if self.__print_info: print ('Info: Download raw df')
                self.raw_df = pd.read_csv(self.full_url, skiprows=2, sep=',')
                self.raw_df = self.raw_df.rename(columns={'Unnamed: 0': 'KPI_General'})

                fname = self.dir_raw_data + 'raw_df_' + str(self.stock_portion_url) + '.csv'
                self.write_df(self.raw_df,fname)
            except:
                if self.__print_debug: print('Problem with processing this data: ', self.full_url)
                self.no_data = True
                if self.__print_debug: print('Prblem with stock: ', self.stock)
                e_1 = sys.exc_info()[0]
                e_2 = sys.exc_info()[1]
                if self.__print_debug: print( "Error: %s with %s" % (e_1, e_2) )
        else:
            self.read_raw_df()
        
        #get yahoo stock values 
        self.get_stock_values()

        
    def get_stock_values(self):
        '''
        extracts the stock data from yahoo and calculates the mean for:
        -last week
        -6 months ago
        -12 month ago
        '''
        try:
            if self.country == 'ger':
                self.stock_yahoo = self.stock + '.DE'
            elif self.country == 'us':
                self.stock_yahoo = self.stock
            elif self.country == 'uk':
                self.stock_yahoo = self.stock + '.L'

            end = dt.date.today()
            yesterday = dt.date.today()
            last_week = dt.date.today() - dt.timedelta(14)
            six_months = dt.date.today() + relativedelta(months=-6)
            six_months_start = six_months-dt.timedelta(7)
            twelve_months = dt.date.today() + relativedelta(months=-12)
            twelve_months_start = twelve_months-dt.timedelta(7)

            self.stock_week = web.get_data_yahoo(self.stock_yahoo, last_week, end )
            self.stock_6_months_ago = web.get_data_yahoo(self.stock_yahoo,six_months_start, six_months )
            self.stock_12_months_ago = web.get_data_yahoo(self.stock_yahoo, twelve_months_start, twelve_months)
            
            self.stock_avg_week = self.stock_week['Adj Close'].mean() 
            self.stock_avg_6_months = self.stock_6_months_ago['Adj Close'].mean() 
            self.stock_avg_12_months = self.stock_12_months_ago['Adj Close'].mean() 

        except:
            if self.__print_debug: print('Problem with yahoo stock extract')
            e_1 = sys.exc_info()[0]
            e_2 = sys.exc_info()[1]
            if self.__print_debug: print( "Error: %s with %s" % (e_1, e_2) )
       

    def load_stock_data(self):
        '''
        1) Combine stock url
        2) Load Data
        '''
        if self.__print_info: print ('Info: Entering load_stock_data')

        self.merge_full_url()
        if self.__print_info: print ('Info:',self.full_url)
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

    def extract_analysis_opinion(self):
        '''
        single function to extract analysis opinon for stocks
        -simple webcrawler gets html content of homepage (yahoo)
        -html is decoded to plain text 
        -plain text is searched for ceratin string
        '''
        import urllib.request as urllib
        import bs4
        import html2text
        
        ao_start_url ='https://de.finance.yahoo.com/q/ao?s='
        if self.country == 'ger':
            ao_portion_url = self.stock + '.DE'
        elif self.country == 'us':
            ao_portion_url = self.stock
        elif self.country == 'uk':
            ao_portion_url = self.stock + '.L'
        ao_url= ao_start_url + ao_portion_url
        beautiful = urllib.urlopen(ao_url).read()

        soup = bs4.BeautifulSoup(beautiful, 'lxml')
        '''
        with open('out.txt', 'w') as f:
            f.write(soup.prettify())
        '''
        
        txt = html2text.html2text(soup.get_text())
        str1 = "Empfehlung (diese Woche):";
        str2 = "Empfehlung (letzte Woche):";
        len_val = 3
        self.str1_and_value = txt[txt.find(str1):txt.find(str1) + len(str1) + len_val]
        self.recommendation_this_week = txt[txt.find(str1)+ len(str1):txt.find(str1) + len(str1) + len_val]
        self.str2_and_value = txt[txt.find(str2):txt.find(str2) + len(str2) + len_val]
        self.recommendation_last_week = txt[txt.find(str2)+ len(str1):txt.find(str2) + len(str2) + len_val]

        if self.recommendation_this_week.replace(',','').isdigit() == True:
            self.recommendation_this_week = self.recommendation_this_week
        else:    
            self.recommendation_this_week = 'NaN'

        self.recommendation_this_week = self.recommendation_this_week.replace(',','.')
        '''
        buy is 1, hold is2, sell is mark 3
        '''



    def plot_data(self,df):
        '''
        Plot some KPIs
        -> still under construction
        '''
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
        '''
        All steps to get the data
        '''
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
                    self.analyze_important_kpis()
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
            timestr = time.strftime("%Y%m%d")
            file_name_end = '_raw_kpi_' + timestr + '.csv'
            self.fname_kpi_collection = self.dir_data + theme + file_name_end
            f = open(self.fname_kpi_collection, 'w')
            writer = csv.writer(f)
            writer.writerow( ('Symbol'
                                , 'RoE'
                                , 'EBIT_Margin'
                                , 'Debt_Equity'
                                , 'P/E 5 years'
                                , 'P/E'
                                , 'Analysis op.' 
                                , 'Reaction Quart.' 
                                , 'Profit revision'
                                , 'Now to 6 months'
                                , 'Now to 12 months'
                                , 'Stock momentum' 
                                , '3 months reversal'
                                , 'Profit growth'
                                , 'EPS'
                                , 'Dividends'
                                , 'Book_value'
                                , 'Stock_avg_week'
                                ) )
            f.close()


        raw_EPS = self.df_full.iloc[5]
        raw_Dividends = self.df_full.iloc[6]
        raw_Book_value = 0
        raw_RoE = self.df_full.iloc[28]
        self.RoE = raw_RoE[raw_RoE.size - 2] #is last year value, -2 due to start at 0 and -1
        raw_EBIT_Margin = self.df_full.iloc[3]
        self.EBIT_Margin = raw_EBIT_Margin[raw_EBIT_Margin.size - 2]
        raw_Dept_Equity = self.df_full.iloc[74]
        self.Dept_Equity = raw_Dept_Equity[raw_Dept_Equity.size - 2]
        self.P_E_5years = self.stock_avg_week / ((float(raw_EPS.TTM) 
                                            + float(raw_EPS[raw_EPS.size-2]) 
                                            + float(raw_EPS[raw_EPS.size-3]) 
                                            + float(raw_EPS[raw_EPS.size-4]) 
                                            + float(raw_EPS[raw_EPS.size-4]))/5)  
        self.P_E = self.stock_avg_week / float(raw_EPS.TTM) 
        #call analysis object
        self.extract_analysis_opinion()
        self.Analysis_op = self.recommendation_this_week
        self.Reaction_quart  = 0
        self.Profit_revision = 0
        self.Now_2_6m = (self.stock_avg_week - self.stock_avg_6_months) / self.stock_avg_week
        self.Now_2_12m = (self.stock_avg_week - self.stock_avg_12_months) / self.stock_avg_week
        if self.Now_2_6m > 0 and self.Now_2_12m <= 0:
            self.Stock_momentum = 1
        elif self.Now_2_6m < 0 and self.Now_2_12m >=0:
            self.Stock_momentum = -1
        else:
            self.Stock_momentum = 0
        self.three_m_reversal = 0
        self.Profit_growth = (float(raw_EPS.TTM) - float(raw_EPS[raw_EPS.size-2]) ) / float(raw_EPS.TTM)


        
        f = open(self.fname_kpi_collection, 'a', newline='')
        writer = csv.writer(f)
        writer.writerow( (self.stock
                            , self.RoE 
                            , self.EBIT_Margin 
                            , self.Dept_Equity
                            , self.P_E_5years
                            , self.P_E
                            , self.Analysis_op
                            , self.Reaction_quart 
                            , self.Profit_revision
                            , self.Now_2_6m
                            , self.Now_2_12m
                            , self.Stock_momentum
                            , self.three_m_reversal
                            , self.Profit_growth
                            , raw_EPS.TTM
                            , raw_Dividends.TTM
                            , raw_Book_value
                            , self.stock_avg_week
                            ) )
        f.close()
        
        #df_test = pd.DataFrame({ 'Symbol' : [self.stock]
        #                        ,'RoE' : [self.RoE]
        #                        })
        #print('hier bin ich') 
        #fname = self.dir_raw_data + 'test' + str(self.stock_portion_url) + '.csv'
        #self.write_df(self.df_test,fname)
        '''
        to do:
        -perfomance accoding to quartalszahlen
        -gewinnrevision
        -dreimonatsreversal(large cap)
        http://quicktake.morningstar.com/StockNet/SECDocuments.aspx?Symbol=CON&Country=deu
        '''

    def analyze_important_kpis(self):

        if self.counter_extract == 0:
            #create files with header
            timestr = time.strftime("%Y%m%d")
            file_name_end = '_analyzed_kpi_' + timestr + '.csv'
            self.fname_kpi_analyze = self.dir_data + theme + file_name_end 
            f = open(self.fname_kpi_analyze, 'w')
            writer = csv.writer(f)
            writer.writerow( ('Symbol'
                                , 'P_Sum'
                                , 'P_RoE'
                                , 'P_EBIT_Margin'
                                , 'P_Dept_Equity'
                                , 'P_P/E 5 years'
                                , 'P_P/E'
                                , 'P_Analysis op.' 
                                , 'P_Reaction Quart.' 
                                , 'P_Profit revision'
                                , 'P_Now to 6 months'
                                , 'P_Now to 12 months'
                                , 'P_Stock momentum' 
                                , 'P_3 months reversal'
                                , 'P_Profit growth'
                                ) )
            f.close()


        self.P_Sum = 0 

        if float(self.RoE) > 20:
            self.P_RoE = 1
            self.P_Sum +=1
        elif float(self.RoE) < 10:
            self.P_RoE = -1
            self.P_Sum -= 1
        else:
            self.P_RoE = 0
        
        if float(self.EBIT_Margin) > 12:
            self.P_EBIT_Margin = 1
            self.P_Sum += 1
        elif float(self.EBIT_Margin) < 6:
            self.P_EBIT_Margin = -1
            self.P_Sum -= 1
        else:
            self.P_EBIT_Margin = 0

        if float(self.Dept_Equity) < 0.75: #here reverse than book
            self.P_Dept_Equity = 1
            self.P_Sum += 1
        elif float(self.Dept_Equity) > 0.85:
            self.P_Dept_Equity = -1
            self.P_Sum -= 1
        else:
            self.P_Dept_Equity = 0

        if float(self.P_E_5years) < 12:
            self.P_P_E_5years = 1
            self.P_Sum += 1
        elif float(self.P_E_5years) > 16:
            self.P_P_E_5years = -1
            self.P_Sum -= 1
        else:
            self.P_P_E_5years = 0
            
        if float(self.P_E) < 12:
            self.P_P_E = 1
            self.P_Sum += 1
        elif float(self.P_E) > 16:
            self.P_P_E = -1
            self.P_Sum -= 1
        else:
            self.P_P_E = 0

        if float(self.Analysis_op) >= 2.5:
            self.P_Analysis_op = 1
            self.P_Sum += 1
        elif float(self.Analysis_op) <= 1.5:
            self.P_Analysis_op = -1
            self.P_Sum -= 1
        else:
            self.P_Analysis_op = 0

        self.P_Reaction_quart = 0
        self.P_Profit_revision = 0

        if float(self.Now_2_6m) > 0.05:
            self.P_Now_2_6m = 1
            self.P_Sum += 1
        elif float(self.Now_2_6m) < -0.05:
            self.P_Now_2_6m = -1
            self.P_Sum -= 1
        else:
            self.P_Now_2_6m = 0

        if float(self.Now_2_12m) > 0.05:
            self.P_Now_2_12m = 1
            self.P_Sum += 1
        elif float(self.Now_2_12m) < -0.05:
            self.P_Now_2_12m = 1
            self.P_Sum -= 1
        else:
            self.P_Now_2_12m = 0

        if float(self.P_Now_2_6m) == 1 and (float(self.P_Now_2_12m) == -1 or float(self.P_Now_2_12m) == 0):
            self.P_Stock_momentum = 1
            self.P_Sum += 1
        elif float(self.P_Now_2_6m) == -1 and (float(self.P_Now_2_12m) == 1 or float(self.P_Now_2_12m) == 0):
            self.P_Stock_momentum -= 1
            self.P_Sum -= 1
        else:
            self.P_Stock_momentum = 0

        self.P_three_m_reversal = 0

        if float(self.Profit_growth) > 0.05:
            self.P_Profit_growth = 1
            self.P_Sum += 1
        elif float(self.Profit_growth) < -0.05:
            self.P_Profit_growth = -1
            self.P_Sum -= 1
        else:
            self.P_Profit_growth = 0
 

        f = open(self.fname_kpi_analyze, 'a', newline='')
        writer = csv.writer(f)
        writer.writerow( (self.stock
                            , self.P_Sum 
                            , self.P_RoE 
                            , self.P_EBIT_Margin 
                            , self.P_Dept_Equity
                            , self.P_P_E_5years
                            , self.P_P_E
                            , self.P_Analysis_op
                            , self.P_Reaction_quart 
                            , self.P_Profit_revision
                            , self.P_Now_2_6m
                            , self.P_Now_2_12m
                            , self.P_Stock_momentum
                            , self.P_three_m_reversal
                            , self.P_Profit_growth
                            ) )
        f.close()
        



    def statistics_important_kpis(self):
        if self.__print_info: print ('Info: Entering analyze_important_kpis')

        self.fname_kpi_collection = self.dir_data + theme + '_' +'kpi_collection.csv'
        self.read_df(self.fname_kpi_collection)
        self.analyze_important_kpis = self.read_df

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
    which_stock_list = 'MDAX'
    #which_stock_list = 'SDAX'
    #which_stock_list = 'TECDAX'
    #which_stock_list = 'NDX100'
    #which_stock_list = 'SP500'
    #which_stock_list = 'FTSE100'
    


    if which_stock_list == 'Test_us':
        country='us' 
        theme = 'TEST_US'
        us_stock_list = ['AMZN', 'GILD' ]
        us_stock_list = ['GILD' ]
        us_stock_list = ['SYMC' ]
        stocks = MS_StatsExtract(country, theme)
        stocks.set_stocklist(us_stock_list)
        stocks.get_data_for_all_stocks()
        stocks.statistics_important_kpis()

    if which_stock_list == 'Test_ger':
        country='ger' 
        theme = 'TEST_GER'
        ger_stock_list = ['CON']
        stocks = MS_StatsExtract(country, theme)
        stocks.set_stocklist(ger_stock_list)
        stocks.get_data_for_all_stocks()

    if which_stock_list == 'MDAX':
        fname = '/Users/Potzenhotz/Dropbox/stock_data/MDAX.csv'
        delimiter = ';'
        country = 'ger' 
        theme = 'MDAX'
        stocks = MS_StatsExtract(country, theme)
        stocks.read_stock_list(fname, delimiter)
        stocks.get_data_for_all_stocks()

    if which_stock_list == 'DAX':
        fname = '/Users/Potzenhotz/Dropbox/stock_data/DAX.csv'
        delimiter = ';'
        country = 'ger' 
        theme = 'DAX'
        stocks = MS_StatsExtract(country, theme)
        stocks.read_stock_list(fname, delimiter)
        stocks.get_data_for_all_stocks()

    if which_stock_list == 'TECDAX':
        fname = '/Users/Potzenhotz/Dropbox/stock_data/TECDAX.csv'
        delimiter = ';'
        country = 'ger' 
        theme = 'TECDAX'
        stocks = MS_StatsExtract(country, theme)
        stocks.read_stock_list(fname, delimiter)
        stocks.get_data_for_all_stocks()


    if which_stock_list == 'SP500':
        fname = '/Users/Potzenhotz/Dropbox/stock_data/' + which_stock_list +'.csv'
        delimiter = ';'
        country = 'us' 
        theme = 'SP500'
        stocks = MS_StatsExtract(country, theme)
        stocks.read_stock_list(fname, delimiter)
        stocks.get_data_for_all_stocks()

    if which_stock_list == 'NDX100':
        fname = '/Users/Potzenhotz/Dropbox/stock_data/' + which_stock_list +'.csv'
        delimiter = ';'
        country = 'us' 
        theme = 'NDX100'
        stocks = MS_StatsExtract(country, theme)
        stocks.read_stock_list(fname, delimiter)
        stocks.get_data_for_all_stocks()

    if which_stock_list == 'FTSE100':
        fname = '/Users/Potzenhotz/Dropbox/stock_data/' + which_stock_list +'.csv'
        delimiter = ';'
        country = 'uk' 
        theme = 'FTSE100'
        stocks = MS_StatsExtract(country, theme)
        stocks.read_stock_list(fname, delimiter)
        stocks.get_data_for_all_stocks()







