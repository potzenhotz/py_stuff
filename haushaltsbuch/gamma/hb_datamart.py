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
 CATEGORY MART: Read and process table
-----------------------------------------------------------------------
'''
print('Start reading and processing category data')
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
                        and substr(t.wertstellung,4,2) = :month\
                        and substr(t.wertstellung,7,4) = :year\
                        and k.konsumkategorie != "Einnahme"\
                        group by k.konsumkategorie_id;'
        #and strftime("%m", t.wertstellung) = :month\
        #and strftime("%Y", t.wertstellung) = :year\

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
            category_mart_df = loaded_core_df
        else:
            category_mart_df = category_mart_df.append(loaded_core_df)
        if_exist = 1

category_mart_df.fillna(0, inplace=True)
print(category_mart_df.columns)
category_mart_df = category_mart_df[['Jahr', 'Monat', 'Konsum', 'Essen', 'Haushalt', 'Bargeld', 'Auto', 'Kreditkarte', 'Firma', 'Sport', 'Urlaub', 'Sonstiges', 'Sparen']]
# get a list of columns
cols = list(category_mart_df)
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('Monat')))
cols.insert(0, cols.pop(cols.index('Jahr')))
# use ix to reorder
category_mart_df = category_mart_df.ix[:, cols]
category_mart_df['Jahr'] = category_mart_df['Jahr'].astype(int)
category_mart_df['Monat'] = category_mart_df['Monat'].astype(int)
'''
-----------------------------------------------------------------------
 MART: Load table
-----------------------------------------------------------------------
'''
print('Start loading year per month data mart')

hb.load_table(category_mart_df, 'dm_ausgaben', haushaltsbuch_db, 'replace', index_type=True)



'''
-----------------------------------------------------------------------
 CATEGORY MART: Read and process table
-----------------------------------------------------------------------
'''
print('Start reading and processing merchant data')
years = list(range(2016,2018))
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',]
kategorien = ['Konsum', 'Essen'] 
for var_kat in kategorien:
    if_exist = 0
    print('STARTING PROCESSING {0}'.format(var_kat))
    for var_year in years:
        for var_month in months:
            core_sql_query = 'select h.haendlerkategorie, sum(t.soll)\
                            from cl_transaktion t, cl_auftraggeber a, cl_haendler h, cl_konsum k\
                            where t.auftraggeber_id = a.auftraggeber_id\
                            and a.haendlerkategorie_id = h.haendlerkategorie_id\
                            and h.konsumkategorie_id = k.konsumkategorie_id\
                            and substr(t.wertstellung,4,2) = :month\
                            and substr(t.wertstellung,7,4) = :year\
                            and k.konsumkategorie != "Einnahme"\
                            and k.konsumkategorie = :kategorie\
                            group by h.haendlerkategorie_id;'
    
            var_ausgaben = 'Ausgaben' 
            result = haushaltsbuch_db.execute(core_sql_query, month=str(var_month), year=str(var_year), kategorie=var_kat)
            #print(result.fetchall())
            loaded_core_df = pd.DataFrame(result.fetchall(), columns=['haendlerkategorie', 'soll'] )
            loaded_core_df.loc[:,'soll'] *= -1
            #print(loaded_core_df.columns)
            if not loaded_core_df.empty:
                loaded_core_df.loc[len(loaded_core_df)]=['Jahr', var_year] 
                loaded_core_df.loc[len(loaded_core_df)]=['Monat', int(var_month)] 
            loaded_core_df.rename(columns={'soll': var_ausgaben}, inplace=True)
            loaded_core_df = loaded_core_df.set_index(['haendlerkategorie'])
            loaded_core_df = loaded_core_df.T
            if if_exist ==  0:
                haendler_mart_df = loaded_core_df
            else:
                haendler_mart_df = haendler_mart_df.append(loaded_core_df)
            if_exist = 1

    haendler_mart_df.fillna(0, inplace=True)
    # get a list of columns
    cols = list(haendler_mart_df)
    # move the column to head of list using index, pop and insert
    cols.insert(0, cols.pop(cols.index('Monat')))
    cols.insert(0, cols.pop(cols.index('Jahr')))
    # use ix to reorder
    haendler_mart_df = haendler_mart_df.ix[:, cols]
    haendler_mart_df['Jahr'] = haendler_mart_df['Jahr'].astype(int)
    haendler_mart_df['Monat'] = haendler_mart_df['Monat'].astype(int)
    print(haendler_mart_df.columns)
    '''
    -----------------------------------------------------------------------
     MART: Load table
    -----------------------------------------------------------------------
    '''
    print('Start loading month category data mart')
    load_table_name = 'dm_' + var_kat.lower()
    hb.load_table(haendler_mart_df, load_table_name, haushaltsbuch_db, 'replace', index_type=True)

