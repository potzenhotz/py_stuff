#!/bin/env python3

#-----------------------------------------------------------------------
# Modules for import
#-----------------------------------------------------------------------
import pandas as pd
from sqlalchemy import create_engine # database connection
import sys
import csv
import numpy as np
import hb_functions as hb
import geopy as geo

#-----------------------------------------------------------------------
#Define input parameters
#-----------------------------------------------------------------------
#input_arguments = sys.argv

#-----------------------------------------------------------------------
#Define database
#-----------------------------------------------------------------------
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')

file_path = '/Users/Potzenhotz/data/raw_data/'
file_name = file_path+'read_data_lines.txt'
with open(file_name) as f:
    file_names = f.read().splitlines()
#file_names.append('Kontoumsaetze_350_355327800_20170114_175539.csv')
#file_names.append('Kontoumsaetze_350_355327800_20170607_174341.csv')
#file_names.append('Kontoumsaetze_350_355327800_20170915_140407.csv')
#file_names.append('test_file.csv')

for file_name in file_names:
    file_full = file_path + file_name
    
    #-----------------------------------------------------------------------
    #STAGING: Read csv
    #-----------------------------------------------------------------------
    staging_df = pd.read_csv(file_full, encoding="ISO-8859-1", sep=';', skiprows=4, skipfooter=1, engine='python')
    
    print(list(staging_df))
    # Convert to datetimes
    # UPDATE: Does not work with duplicate diff load -> therfore we stay with strings
    #staging_df['Buchungstag'] = pd.to_datetime(staging_df["Buchungstag"],format="%d.%m.%Y")
    #staging_df['Wertstellung'] = pd.to_datetime(staging_df["Wertstellung"],format="%d.%m.%Y")
    
    staging_df.rename(columns={'Wert': 'wertstellung'}, inplace=True)
    staging_df.rename(columns={'Begünstigter / Auftraggeber': 'auftraggeber'}, inplace=True)
    staging_df.rename(columns={'Währung': 'waehrung'}, inplace=True)
    staging_df.rename(columns={'Soll': 'soll'}, inplace=True)
    staging_df.rename(columns={'Haben': 'haben'}, inplace=True)
    staging_df.rename(columns={'Verwendungszweck': 'verwendungszweck'}, inplace=True)
    staging_df.rename(columns={'Buchungstag': 'buchungstag'}, inplace=True)
    staging_df.rename(columns={'Umsatzart': 'umsatzart'}, inplace=True)
    
    staging_df['soll'].fillna('0,0', inplace=True)
    staging_df['haben'].fillna('0,0', inplace=True)
    
    #staging_df['Umsatzart'].fillna(np.NaN, inplace=True)
    #staging_df['auftraggeber'].fillna(np.NaN, inplace=True)
    #staging_df['IBAN'].fillna(np.NaN, inplace=True)
    #staging_df['BIC'].fillna(np.NaN, inplace=True)
    
    #staging_df['Umsatzart'].fillna(None, inplace=True)
    #staging_df['auftraggeber'].fillna(None, inplace=True)
    #staging_df['IBAN'].fillna(None, inplace=True)
    #staging_df['BIC'].fillna(None, inplace=True)
    
    staging_df['soll'] = staging_df['soll'].str.replace('.', '')
    staging_df['soll'] = staging_df['soll'].str.replace(',', '.')
    staging_df['soll'] = staging_df['soll'].astype(float)
    
    staging_df['haben'] = staging_df['haben'].str.replace('.', '')
    staging_df['haben'] = staging_df['haben'].str.replace(',', '.')
    staging_df['haben'] = staging_df['haben'].astype(float)
    
    
    
    staging_df['new_flag'] = '1'
    '''
    -----------------------------------------------------------------------
     STAGING: drop columns
    -----------------------------------------------------------------------
    '''
    #0 for rows and 1 for columns
    staging_df = staging_df.drop('Kundenreferenz', 1)
    staging_df = staging_df.drop('Mandatsreferenz ', 1)
    staging_df = staging_df.drop('Gläubiger ID', 1)
    staging_df = staging_df.drop('Fremde Gebühren', 1)
    staging_df = staging_df.drop('Betrag', 1)
    staging_df = staging_df.drop('Abweichender Empfänger', 1)
    staging_df = staging_df.drop('Anzahl der Aufträge', 1)
    staging_df = staging_df.drop('Anzahl der Schecks', 1)
    
    #-----------------------------------------------------------------------
    # STAGING: Modify rows and columns
    #-----------------------------------------------------------------------
    #ACHTUNG CHANGES WERDEN ERST NACH DEM LOOP COMMITED
    #DAHER REIHENFOLGE WICHTIG
    
    uebersetzung_sql_query = 'select raw_value, uebersetzung from ht_uebersetzung' 
    uebersetzung_df = hb.read_sql(haushaltsbuch_db, uebersetzung_sql_query)
    print(list(uebersetzung_df))
    
    auftraggeber_sql_query = 'select raw_value, auftraggeber from ht_auftraggeber' 
    auftraggeber_df = hb.read_sql(haushaltsbuch_db, auftraggeber_sql_query)
    print(list(auftraggeber_df))
    
    staedte_sql_query = 'select raw_value, stadt from ht_staedte' 
    staedte_df = hb.read_sql(haushaltsbuch_db, staedte_sql_query)
    print(list(staedte_df))
    
    staging_df.insert( 4, 'stadt', None)
    staging_df.insert( 5, 'land', None)
    
    for index, row in staging_df.iterrows():
        if pd.isnull(row['auftraggeber']):
            staging_df.set_value(index,'auftraggeber', row['verwendungszweck'].split('/')[0])
    
        length_verw=len(row['verwendungszweck'].split('/'))
        if length_verw > 2:
            for s_index, s_row in staedte_df.iterrows():
                if row['verwendungszweck'].split('/')[2].find(s_row['raw_value']) !=-1:
                    staging_df.set_value(index,'stadt', s_row['stadt'])
                    break
        elif length_verw == 2:
            for s_index, s_row in staedte_df.iterrows():
                if row['verwendungszweck'].split('/')[1].find(s_row['raw_value']) !=-1:
                    staging_df.set_value(index,'stadt', s_row['stadt'])
                    break
    
        for u_index, u_row in uebersetzung_df.iterrows():
            if row['verwendungszweck'].find(u_row['raw_value']) != -1:
                staging_df.set_value(index,'auftraggeber',u_row['uebersetzung'])
                if u_row['raw_value'] == 'KREDITKARTE':
                    staging_df.set_value(index,'umsatzart',u_row['uebersetzung'])
    
        if not pd.isnull(row['umsatzart']):
            if row['umsatzart'].find('Auszahlung Geldautomat') != -1:
                staging_df.set_value(index,'auftraggeber', 'Auszahlung Geldautomat')
        
        if row['verwendungszweck'].find('Auszahlung') != -1:
            staging_df.set_value(index,'auftraggeber', 'Auszahlung Geldautomat')
            staging_df.set_value(index,'umsatzart', 'Auszahlung Geldautomat')
            
    
    for index, row in staging_df.iterrows():
        if not pd.isnull(row['auftraggeber']):
            for a_index, a_row in auftraggeber_df.iterrows():
                try:
                    if row['auftraggeber'].find(a_row['raw_value']) != -1:
                        staging_df.set_value(index,'auftraggeber',a_row['auftraggeber'])
                except:
                    print('except in for loop for ht_auftraggeber',row['auftraggeber'])
    
    
    #-----------------------------------------------------------------------
    # STAGING: Load table
    #-----------------------------------------------------------------------
    print(list(staging_df))
    
    columns = ['wertstellung', 'verwendungszweck']
    load_staging_df = hb.clean_df_db_dups(staging_df, 'sl_DeuBa', haushaltsbuch_db, columns) 
    print('Head of loaded df: \n',load_staging_df.head()) 
    #load_staging_df['buchungstag'] = pd.to_datetime(staging_df["buchungstag"],format="%d.%m.%Y")
    #load_staging_df['wertstellung'] = pd.to_datetime(staging_df["wertstellung"],format="%d.%m.%Y")
    hb.load_table(load_staging_df, 'sl_DeuBa', haushaltsbuch_db, 'append')

