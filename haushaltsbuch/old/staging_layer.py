#!/bin/env python3
'''
Staging Layer
'''
import pandas as pd
from sqlalchemy import create_engine # database connection
import sys
import csv
import numpy as np
import petl as etl

'''
Define input parameters
'''
input_arguments = sys.argv
par_load = 'replace'
file_path = '/Users/Potzenhotz/data/raw_data/'
file_name = 'Kontoumsaetze_350_355327800_20170114_175539.csv'
file_name = 'Kontoumsaetze_350_355327800_20170204_010626.csv'
file_name = 'Kontoumsaetze_350_355327800_20170211_173521.csv'
file_full = file_path + file_name

'''
Define input parameters
'''
#staging_layer_db = create_engine('sqlite:////Users/Potzenhotz/data/database/staging_layer.db')
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')

'''
Define input parameters
'''
raw_df = pd.read_csv(file_full, encoding="ISO-8859-1", sep=';', skiprows=4, skipfooter=1, engine='python')

# Convert to datetimes
raw_df['Buchungstag'] = pd.to_datetime(raw_df['Buchungstag'], format='%d.%m.%Y')
raw_df['Wert'] = pd.to_datetime(raw_df['Wert'], format='%d.%m.%Y')
raw_df.rename(columns={'Wert': 'Wertstellung'}, inplace=True)
raw_df.rename(columns={'Begünstigter / Auftraggeber': 'BeguenstigterAuftraggeber'}, inplace=True)

#raw_df['Umsatzart'].fillna('no data', inplace=True)
#raw_df['BeguenstigterAuftraggeber'].fillna('no data', inplace=True)
#raw_df['IBAN'].fillna('no data', inplace=True)
#raw_df['BIC'].fillna('no data', inplace=True)
raw_df['Soll'].fillna('0,0', inplace=True)
raw_df['Haben'].fillna('0,0', inplace=True)

raw_df['Umsatzart'].fillna(np.NaN, inplace=True)
raw_df['BeguenstigterAuftraggeber'].fillna(np.NaN, inplace=True)
raw_df['IBAN'].fillna(np.NaN, inplace=True)
raw_df['BIC'].fillna(np.NaN, inplace=True)

raw_df['Soll'] = raw_df['Soll'].str.replace('.', '')
raw_df['Soll'] = raw_df['Soll'].str.replace(',', '.')
raw_df['Soll'] = raw_df['Soll'].astype(float)

raw_df['Haben'] = raw_df['Haben'].str.replace('.', '')
raw_df['Haben'] = raw_df['Haben'].str.replace(',', '.')
raw_df['Haben'] = raw_df['Haben'].astype(float)


if par_load == 'replace':
    raw_df.to_sql('staging_layer', haushaltsbuch_db, if_exists='replace', index=False)
elif par_load == 'append':
    raw_df.to_sql('staging_layer', haushaltsbuch_db, if_exists='append', index=False)

