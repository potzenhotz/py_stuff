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
file_name = 'Kontoumsaetze_350_355327800_20170114_175539.csv'
file_full = file_path + file_name

#-----------------------------------------------------------------------
#STAGING: Read csv
#-----------------------------------------------------------------------
staging_df = pd.read_csv(file_full, encoding="ISO-8859-1", sep=';', skiprows=4, skipfooter=1, engine='python')

# Convert to datetimes
# UPDATE: Does not work with duplicate diff load -> therfore we stay with strings
#staging_df['Buchungstag'] = pd.to_datetime(staging_df["Buchungstag"],format="%d.%m.%Y")
#staging_df['Wertstellung'] = pd.to_datetime(staging_df["Wertstellung"],format="%d.%m.%Y")

staging_df.rename(columns={'Wert': 'Wertstellung'}, inplace=True)
staging_df.rename(columns={'Begünstigter / Auftraggeber': 'Auftraggeber'}, inplace=True)
staging_df.rename(columns={'Währung': 'Waehrung'}, inplace=True)

staging_df['Soll'].fillna('0,0', inplace=True)
staging_df['Haben'].fillna('0,0', inplace=True)

#staging_df['Umsatzart'].fillna(np.NaN, inplace=True)
#staging_df['Auftraggeber'].fillna(np.NaN, inplace=True)
#staging_df['IBAN'].fillna(np.NaN, inplace=True)
#staging_df['BIC'].fillna(np.NaN, inplace=True)

#staging_df['Umsatzart'].fillna(None, inplace=True)
#staging_df['Auftraggeber'].fillna(None, inplace=True)
#staging_df['IBAN'].fillna(None, inplace=True)
#staging_df['BIC'].fillna(None, inplace=True)

staging_df['Soll'] = staging_df['Soll'].str.replace('.', '')
staging_df['Soll'] = staging_df['Soll'].str.replace(',', '.')
staging_df['Soll'] = staging_df['Soll'].astype(float)

staging_df['Haben'] = staging_df['Haben'].str.replace('.', '')
staging_df['Haben'] = staging_df['Haben'].str.replace(',', '.')
staging_df['Haben'] = staging_df['Haben'].astype(float)



staging_df['new_flag'] = '1'

#-----------------------------------------------------------------------
# STAGING: drop columns
#-----------------------------------------------------------------------
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


staedte_sql_query = 'select raw_value, stadt from ht_staedte' 
staedte_df = hb.read_sql(haushaltsbuch_db, staedte_sql_query)
print(list(staedte_df))


#staging_df['Stadt'] = None
#staging_df['Land'] = 'no_data'
staging_df.insert( 4, 'Stadt', None)
staging_df.insert( 5, 'Land', None)

for index, row in staging_df.iterrows():
    if pd.isnull(row['Auftraggeber']):
        staging_df.set_value(index,'Auftraggeber', row['Verwendungszweck'].split('/')[0])

    length_verw=len(row['Verwendungszweck'].split('/'))
    #print(length_verw)
    if length_verw > 2:
        for s_index, s_row in staedte_df.iterrows():
            if row['Verwendungszweck'].split('/')[2].find(s_row['raw_value']) !=-1:
                staging_df.set_value(index,'Stadt', s_row['stadt'])
                #print(row['Verwendungszweck'].split('/')[2], key, value, index)
                break
    elif length_verw == 2:
        for s_index, s_row in staedte_df.iterrows():
            if row['Verwendungszweck'].split('/')[1].find(s_row['raw_value']) !=-1:
                staging_df.set_value(index,'Stadt', s_row['stadt'])
                #print('###',row['Verwendungszweck'].split('/')[1], key, value, index)
                break


    for u_index, u_row in uebersetzung_df.iterrows():
        if row['Verwendungszweck'].find(u_row['raw_value']) != -1:
            staging_df.set_value(index,'Auftraggeber',u_row['uebersetzung'])
            if u_row['raw_value'] == 'KREDITKARTE':
                staging_df.set_value(index,'Umsatzart',u_row['uebersetzung'])

    #if row['Umsatzart'] is not None:
    #if not row['Umsatzart']:
    if not pd.isnull(row['Umsatzart']):
        if row['Umsatzart'].find('Auszahlung Geldautomat') != -1:
            staging_df.set_value(index,'Auftraggeber', 'Auszahlung Geldautomat')


#-----------------------------------------------------------------------
# STAGING: Load table
#-----------------------------------------------------------------------
print(list(staging_df))

columns = ['Wertstellung', 'Verwendungszweck']
load_staging_df = hb.clean_df_db_dups(staging_df, 'sl_DeuBa', haushaltsbuch_db, columns) 
print('Head of loaded df: \n',load_staging_df.head()) 
hb.load_table(load_staging_df, 'sl_DeuBa', haushaltsbuch_db, 'append')

