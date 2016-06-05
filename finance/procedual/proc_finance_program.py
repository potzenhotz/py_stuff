#!/usr/bin/env python
#from yahoo_finance import Share
#-----------------------------------------------------------------------
#Modules
#-----------------------------------------------------------------------
import sys
import pandas as pd
import pandas_datareader.data as web
import proc_finance_load as fl
import datetime as dt
import csv
import scipy as sc
from scipy import stats
import statsmodels.api as sm
import numpy as np
import time
import plot_function as pf

#-----------------------------------------------------------------------
#Parameters
#-----------------------------------------------------------------------
print('Parameter values')
par_reload_data = True
par_reload_data = False
print('Reload data:', par_reload_data)

par_price_norm = True
par_price_norm = False
print('Normalized data:', par_price_norm)

par_recalc_regression = True
#par_recalc_regression = False
print('Recalc regression data:', par_recalc_regression)

par_plot = True
#par_plot = False
print('Plot Data:', par_plot)

if par_plot:
    par_save_plot_top10 = True
    #par_save_plot_top10 = False

    par_save_plot_last10 = True
    #par_save_plot_last10 = False

    par_save_plot_top50 = True
    par_save_plot_top50 = False


par_start_time = 2013
#par_start_time = 2015
print('Start time:', par_start_time)

par_nasdaq = True
#par_nasdaq = False

print('--------------------------------')
#sys.exit("Stoped here")
#-----------------------------------------------------------------------
#Define to be loaded stocks
#-----------------------------------------------------------------------
print('Load ticker list!')
t_stocks = ['AAPL', 'IBM', 'MSFT', 'GOOG', 'NTT.F']
raw_ticker_list  = pd.read_csv('/Users/Potzenhotz/python/finance/nasdaqlisted.csv',delimiter='|')

ticker_list = pd.DataFrame(raw_ticker_list)

print('--------------------------------')
#-----------------------------------------------------------------------
#Reload or read data for stocks
#-----------------------------------------------------------------------
print('Load Data!')
start_2013 = dt.datetime(2013,1,1).date()
start_2015 = dt.datetime(2015,1,1).date()
end = dt.datetime.today()
if par_nasdaq:
    price_nasdaq_2013 = fl.get_price(par_reload_data, ticker_list.Symbol, start_2013, end)
    price_nasdaq_2015 = fl.get_price(par_reload_data, ticker_list.Symbol, start_2015, end)

if (par_start_time == 2013):
    price = price_nasdaq_2013
    start = start_2013
elif (par_start_time == 2015):
    price = price_nasdaq_2015
    start = start_2015

print('--------------------------------')
#-----------------------------------------------------------------------
#Data cleansing
#-----------------------------------------------------------------------
print('Data Cleansing!')
n_stock_x = price.columns[1::]#first index has Date

for stocks in n_stock_x:
    if price[stocks].isnull().sum() > (price[stocks].index[-1])/2:
        del price[stocks]

#Reset Stocks
n_stock_x = price.columns[1::]#first index has Date

print('--------------------------------')
#-----------------------------------------------------------------------
#Data analytics
#-----------------------------------------------------------------------
print('Data Analytics!')
if par_price_norm:
    price_norm =( (price[n_stock_x] 
                  - price[n_stock_x].mean()) 
                  / (price[n_stock_x].max() 
                  - price[n_stock_x].min())
                )
    
#Transform Date_string to Datetime
price['Date'] = pd.to_datetime(price['Date'])

#Option to replace nan with 0
#price = price.fillna(0)

#calc days from start d_start+1
#price['Date_delta'] = (price['Date'] - price['Date'].min())  / np.timedelta64(1,'D')

f_loc = '/Users/Potzenhotz/python/finance/data/'
f_title_regr = 'regr_data' + str(start) + '.csv'
f_name_regr = f_loc + f_title_regr
f_title_regr_top10 = 'regr_data_top10' + str(start) + '.csv'
f_name_regr_top10 = f_loc + f_title_regr_top10
f_title_regr_top50 = 'regr_data_top50' + str(start) + '.csv'
f_name_regr_top50 = f_loc + f_title_regr_top50
if par_recalc_regression:
    x=price.index
    regr_data = {}
    for stocks in n_stock_x:
        y=price[stocks]
        #mask the nan values for regression
        xm = np.ma.masked_array(x,mask=np.isnan(y)).compressed()
        ym = np.ma.masked_array(y,mask=np.isnan(y)).compressed()
        #y=price_norm[stocks]
        regressionline = sc.stats.linregress(xm,ym)
        regr_data[stocks] = [regressionline[0]
                            , regressionline[1]
                            , regressionline[2]
                            ]
    regr_df = pd.DataFrame(regr_data)
    regr_df = regr_df.transpose()
    regr_df.columns = ['slope', 'intercept', 'r-value']

    regr_top10 = regr_df.sort_values(by='slope', ascending=False)[:10]
    regr_top50 = regr_df.sort_values(by='slope', ascending=False)[:50]
    regr_last10 = regr_df.sort_values(by='slope', ascending=True)[:10]

    regr_df.to_csv(f_name_regr)               
    regr_top10.to_csv(f_name_regr_top10)               
    regr_top50.to_csv(f_name_regr_top50)               
else:
    regr_df = pd.read_csv(f_name_regr, index_col=0)
    regr_top10 = pd.read_csv(f_name_regr_top10, index_col=0)
    regr_top50 = pd.read_csv(f_name_regr_top50, index_col=0)


good_stock = regr_top10['slope'].idxmax()
m = regr_df.ix[good_stock].slope
b = regr_df.ix[good_stock].intercept
x_ff = price.index
#sys.exit("Stoped here")
print('--------------------------------')
#-----------------------------------------------------------------------
#Plotting
#-----------------------------------------------------------------------
print('Plotting!')
def do_plot(regr_plot, title_part, folder):
    for plot_stocks in regr_plot.index:
        m = regr_plot.ix[plot_stocks].slope
        b = regr_plot.ix[plot_stocks].intercept
        x_ff = price.index
        title = title_part + plot_stocks + '_' + str(start)
        pf.plot_func_2(price['Date'], price[plot_stocks], price['Date'], m*x_ff+b, title, folder)


if par_plot:
    if par_save_plot_top10:
        folder = 'plots/top10/'
        do_plot(regr_top10, 'top10_', folder)
    if par_save_plot_last10:
        folder = 'plots/last10/'
        do_plot(regr_last10, 'last10_', folder)
    if par_save_plot_top50:
        folder = 'plots/top50/'
        do_plot(regr_top50, 'top50_', folder)
         


print('--------------------------------')
#-----------------------------------------------------------------------
#Status
#-----------------------------------------------------------------------
#print('These are the stocks: %s' %(price.columns))
#print('The data_index starts at %s and ends at %s' %(price.index[0],price.index[-1]))
#print(regr_top10)
