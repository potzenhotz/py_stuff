'''
-----------------------------------------------------------------------
 Modules for import
-----------------------------------------------------------------------
'''
import pandas as pd
from sqlalchemy import create_engine, MetaData 
import sys
import csv
import numpy as np
import hb_functions as hb
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('seaborn-pastel')
print(matplotlib.get_configdir())
#plt.style.use('https://gist.githubusercontent.com/rhiever/d0a7332fe0beebfdc3d5/raw/\
#                205e477cf231330fe2f265070f7c37982fd3130c/tableau10.mplstyle')
#from palettable.colorbrewer.qualitative import Dark2_7

#print(plt.style.available)
'''
#-----------------------------------------------------------------------
#Define database
#-----------------------------------------------------------------------
'''
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')

'''
-----------------------------------------------------------------------
 MART: Read and process table
-----------------------------------------------------------------------
'''
print('Start reading and processing data')
#range(start,end+1)
years = list(range(2016,2018))
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',]
if_exist = 0
for var_year in years:
    for var_month in months:
        core_sql_query = 'select k.konsumkategorie, sum(t.soll)\
                        from cl_transaktion t, cl_auftraggeber a, cl_haendler h, cl_konsum k\
                        where t.auftraggeber_id = a.auftraggeber_id\
                        and a.haendlerkategorie_id = h.haendlerkategorie_id\
                        and h.konsumkategorie_id = k.konsumkategorie_id\
                        and strftime("%m", t.wertstellung) = :month\
                        and strftime("%Y", t.wertstellung) = :year\
                        and k.konsumkategorie != "Einnahme"\
                        group by k.konsumkategorie_id;'

        var_ausgaben = 'Ausgaben' 
        result = haushaltsbuch_db.execute(core_sql_query, month=str(var_month), year=str(var_year))
        loaded_core_df = pd.DataFrame(result.fetchall(), columns=['konsumkategorie', 'soll'] )
        loaded_core_df.loc[:,'soll'] *= -1
        if not loaded_core_df.empty:
            loaded_core_df.loc[len(loaded_core_df)]=['Jahr', var_year] 
            loaded_core_df.loc[len(loaded_core_df)]=['Monat', int(var_month)] 
        loaded_core_df.rename(columns={'soll': var_ausgaben}, inplace=True)
        loaded_core_df = loaded_core_df.set_index(['konsumkategorie'])
        loaded_core_df = loaded_core_df.T
        if if_exist ==  0:
            mart_df = loaded_core_df
        else:
            mart_df = mart_df.append(loaded_core_df)
        if_exist = 1

mart_df.fillna(0, inplace=True)
mart_df = mart_df[['Jahr', 'Monat', 'Konsum', 'Essen', 'Haushalt', 'Bargeld', 'Auto', 'Kreditkarte', 'Firma'\
                    , 'Sport', 'Urlaub', 'Sonstiges']]
mart_df['Jahr'] = mart_df['Jahr'].astype(int)
mart_df['Monat'] = mart_df['Monat'].astype(int)
'''
-----------------------------------------------------------------------
 MART: Load table
-----------------------------------------------------------------------
'''
print('Start loading data mart')

hb.load_table(mart_df, 'dm_konsum', haushaltsbuch_db, 'replace', index_type=True)


