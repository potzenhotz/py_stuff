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
import geopy

#-----------------------------------------------------------------------
#Define input parameters
#-----------------------------------------------------------------------
#input_arguments = sys.argv
par_load = 'append' #for integration layer
par_load = 'initial' #for integration layer
file_path = '/Users/Potzenhotz/data/raw_data/'
file_name = 'Kontoumsaetze_350_355327800_20170114_175539.csv'
file_name = 'Kontoumsaetze_350_355327800_20170204_010626.csv'
file_name = 'Kontoumsaetze_350_355327800_20170211_173521.csv'
file_full = file_path + file_name

#-----------------------------------------------------------------------
#Define database
#-----------------------------------------------------------------------
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')

#-----------------------------------------------------------------------
#STAGING: Read csv
#-----------------------------------------------------------------------
raw_df = pd.read_csv(file_full, encoding="ISO-8859-1", sep=';', skiprows=4, skipfooter=1, engine='python')

# Convert to datetimes
raw_df['Buchungstag'] = pd.to_datetime(raw_df['Buchungstag'], format='%d.%m.%Y')
raw_df['Wert'] = pd.to_datetime(raw_df['Wert'], format='%d.%m.%Y')
raw_df.rename(columns={'Wert': 'Wertstellung'}, inplace=True)
raw_df.rename(columns={'Begünstigter / Auftraggeber': 'BeguenstigterAuftraggeber'}, inplace=True)

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


#-----------------------------------------------------------------------
# STAGING: Load table
#-----------------------------------------------------------------------
hb.load_table(raw_df, 'staging_layer', haushaltsbuch_db, 'replace')


#-----------------------------------------------------------------------
# INTEGRATION: Read table
#-----------------------------------------------------------------------
raw_il_sql_query = 'select buchungstag, wertstellung, umsatzart, beguenstigterauftraggeber\
                , verwendungszweck, iban, bic, soll, haben, währung from staging_layer;'

raw_il_df = hb.read_sql(haushaltsbuch_db, raw_il_sql_query)

#-----------------------------------------------------------------------
# INTEGRATION: Modify rows and columns
#-----------------------------------------------------------------------
#ACHTUNG CHANGES WERDEN ERST NACH DEM LOOP COMMITED
#DAHER REIHENFOLGE WICHTIG
uebersetzung = {'KREDITKARTE': 'Kreditkarte','Miete Lukas Lübeck': 'Miete'
                , 'monatliche Sparrate':'ETF-Sparplan', 'Sparbuch': 'Sparbuch', 'Auxmoney':'Auxmoney'
                , 'Miete und Co': 'Miete', 'Monatliche Einzahlung':'Miete', 'Sparen':'Sparbuch'
                , 'Aktien':'Aktien', 'Akiten':'Aktien'}

staedte = {'KARLSRUHE':'Karlsruhe', 'Dortmund Kley':'Dortmund', 'LUEBECK':'Luebeck'
        ,'DORTMUND':'Dortmund', 'KASSEL':'Kassel', 'SANDESNEBEN':'Sandesneben'
        , 'Luebeck':'Luebeck', 'QUARTU SANT':'Cagiliari'}

raw_il_df['Stadt'] = 'no_data'
raw_il_df['Land'] = 'no_data'

for index, row in raw_il_df.iterrows():
    if pd.isnull(row['BeguenstigterAuftraggeber']):
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber', row['Verwendungszweck'].split('/')[0])

    length_verw=len(row['Verwendungszweck'].split('/'))
    if length_verw > 2:
        for key, value in staedte.items():
            if row['Verwendungszweck'].split('/')[2].find(key) !=-1:
                raw_il_df.set_value(index,'Stadte', value)
            #else:
            #    raw_il_df.set_value(index,'Ort', row['Verwendungszweck'].split('/')[2])
    elif length_verw == 2:
        for key, value in staedte.items():
            if row['Verwendungszweck'].split('/')[1].find(key) !=-1:
                raw_il_df.set_value(index,'Stadt', value)
    #        else:
    #            raw_il_df.set_value(index,'Ort', row['Verwendungszweck'].split('/')[1])


    for key, value in uebersetzung.items():
        if row['Verwendungszweck'].find(key) != -1:
            raw_il_df.set_value(index,'BeguenstigterAuftraggeber',value)
            if key == 'KREDITKARTE':
                raw_il_df.set_value(index,'Umsatzart',value)

    if row['Umsatzart'] is not None:
        if row['Umsatzart'].find('Auszahlung Geldautomat') != -1:
            raw_il_df.set_value(index,'BeguenstigterAuftraggeber', 'Auszahlung Geldautomat')

#-----------------------------------------------------------------------
# INTEGRATION: Load table
#-----------------------------------------------------------------------
if par_load == 'initial':
    hb.load_table(raw_il_df, 'integration_layer', haushaltsbuch_db, 'replace')
elif par_load == 'append':
    columns = ['Wertstellung', 'Verwendungszweck']
    load_il_df = hb.clean_df_db_dups(raw_il_df, 'integration_layer', haushaltsbuch_db, columns) 
    hb.load_table(load_il_df, 'integration_layer', haushaltsbuch_db, 'append')


#-----------------------------------------------------------------------
# CORE: Read table
#-----------------------------------------------------------------------
il_sql_query = 'select wertstellung, umsatzart, beguenstigterauftraggeber, verwendungszweck\
                        , iban, bic, soll, haben, währung, stadt from integration_layer;'

il_df = hb.read_sql(haushaltsbuch_db, il_sql_query)

#Create Keys for certain rows
il_df['Kategorie_ID'] = pd.factorize(il_df.BeguenstigterAuftraggeber)[0]
il_df['Umsatzart_ID'] = pd.factorize(il_df.Umsatzart)[0]
il_df['Ort_ID'] = pd.factorize(il_df.Stadt)[0]

transaction_df = il_df[['Umsatzart_ID', 'Kategorie_ID', 'Ort_ID'
                        , 'Soll', 'Haben', 'Wertstellung']].copy()
revenue_type_df = il_df[['Umsatzart_ID','Umsatzart']].copy()
places_df = il_df[['Ort_ID','Stadt']].copy()
category_df = il_df[['Kategorie_ID','BeguenstigterAuftraggeber']].copy()

category_df.drop_duplicates(inplace=True)
revenue_type_df.drop_duplicates(inplace=True)
places_df.drop_duplicates(inplace=True)
category_df['Kategorie'] = 'no_data'
category_df['Haendler'] = 'no_data'

#-----------------------------------------------------------------------
# CORE: Define categories
#-----------------------------------------------------------------------
category_konsum = {'P+C':'Kleidung', 'H+M':'Kleidung', 'HM':'Kleidung', 'RIMOWA':'Rimowa','SPOT':'Rest'
                    , 'PEEK+CLOPPENBURG':'Kleidung'
                    , 'DM':'Drogerie', 'HUGENDUBEL':'Buecher', 'DOUGLAS':'Drogerie', 'TKmaxx':'Kleidung'
                    , 'SATURN':'Elektronik', 'ROSSMANN':'Drogerie'
                    , 'SCHUH BODE':'Kleidung', 'WEINHANDLUNG':'Spirituosen', 'BVB':'Rest'
                    , 'MAYERSCHE':'Buecher', 'STAPLES':'Schreibwaren', 'AMAZON':'Amazon'
                    , 'PayPal':'Paypal', 'DECATHLON':'Kleidung', 'ERWIN MATUTT':'Rest'
                    , 'Geco':'Lotto'}

category_essen = {'METRO':'Einkauf', 'BLAUER ENGEL':'Restautrant', 'WINGAS':'Restaurant', 'REWE':'Einkauf'
                    , 'EDEKA':'Einkauf'
                    , 'AUCHAN':'Einkauf', 'HOLIDAY INN LUEBECK':'Restaurant', 'Jung + Frech':'Restaurant'
                    , 'Vapiano':'Restaurant'
                    , 'RESTAURANT':'Restaurant', 'famila':'Einkauf', 'SUSHI':'Restaurant'
                    , 'RASTANLAGE':'Restaurant', 'REAL':'Einkauf'
                    , 'Osteria':'Restaurant', 'ALDI':'Einkauf', 'LIDL':'Einkauf', 'Auchan':'Einkauf'
                    , 'SUPERMERCATO':'Einkauf', 'CITTI':'Einkauf'}

category_haushalt = { 'congstar':'Handy', 'BAUHAUS':'Baumarkt', 'HELLWEG':'Baumarkt'
                    , 'DB Vertrieb':'Mobility'
                    , 'BEZIRKSREGIERUNG':'Steuern', 'Miete':'Miete', 'Abschlussposten':'Bank' }


category_auto = { 'SHELL':'Tanken', 'SB Tank':'Tanken', 'AVIA':'Tanken', 'OIL TANK':'Tanken'
                    , 'Orlen':'Tanken', 'JET':'Tanken'
                    , 'HDI':'Versicherung', 'BUNDESKASSE IN KIEL':'Steuern', 'Westfalen TS':'Tanken' }

category_firma = { 'Flughafen Hamburg':'Parken', 'Payco Taxi':'Taxi'
                    , 'VBK-VERKEHRSBETRIEBE KARLS':'Mobility' }

category_sport = { 'McFIT':'Fitnessstudio', 'FitX':'Fitnessstudio' }

category_sonstiges = { 'TABAK':'Sonstiges' }

category_einnahme = {'NTT':'Gehalt', 'LUISE':'Oma'}

category_kreditkarte = { 'Kreditkarte':'Kreditkarte' }

category_bargeld = {'Auszahlung':'Auszahlung'}

category_sparen = {'ETF-Sparplan':'Sparplan', 'Sparbuch':'Sparbuch', 'Auxmoney':'Auxmoney'
                    , 'Aktien':'Aktien'}

category_alex_lukas = {'IKEA':'Moebel', 'FUENFUNDDREISSIG':'Sonstiges', 'Verk.iersverbond':'Mobility'
                        , 'PEAK PERFORMANCE GBG':'Kleidung'
                        , 'Fink, Arne':'Moebel', 'Frieda Bühl':'Miete', 'KUECHE 1':'Moebel'}

category_urlaub = {'MORISCA':'Urlaub', 'Urlaub':'Urlaub', 'Viktoria Boss':'Skiurlaub'}


category_undefined = {'no_data':'no_data'}


category_dict = {'Konsum':category_konsum, 'Eseen':category_essen, 'Haushalt':category_haushalt
                , 'Sport':category_sport , 'Firma':category_firma, 'Sonstiges':category_sonstiges
                , 'Einnahme':category_einnahme, 'Kreditkarte':category_kreditkarte
                , 'Bargeld':category_bargeld, 'Sparen':category_sparen
                , 'Alex+Lukas': category_alex_lukas, 'Urlaub': category_urlaub
                , 'Auto': category_auto}

#-----------------------------------------------------------------------
# CORE: Modify rows and columns
#-----------------------------------------------------------------------
transaction_df.rename(columns={"Soll": "Ausgaben", "Haben": "Einnahmen"},inplace=True)


for index, row in category_df.iterrows():
    for key, value in category_dict.items():
        for v_key, v_value in value.items():
            if row['BeguenstigterAuftraggeber'].find(v_key) != -1:
                category_df.set_value(index,'Kategorie', key)
                category_df.set_value(index,'Haendler', v_value)

for index, row in category_df.iterrows():
    for k_undefined, v_undefined in category_undefined.items():
        if row['Kategorie'].find(k_undefined) != -1:
            category_df.set_value(index,'Kategorie', 'Undefiniert')
            category_df.set_value(index,'Haendler', 'Undefiniert')

#-----------------------------------------------------------------------
# CORE: Load table
#-----------------------------------------------------------------------
hb.load_table(transaction_df, 'cl_transactions', haushaltsbuch_db, 'replace')
hb.load_table(revenue_type_df, 'cl_revenue_types', haushaltsbuch_db, 'replace')
hb.load_table(places_df, 'cl_places', haushaltsbuch_db, 'replace')
hb.load_table(category_df, 'cl_categories', haushaltsbuch_db, 'replace')



#-----------------------------------------------------------------------
# DATA MART: Read table
#-----------------------------------------------------------------------
t_sql_query = 'select umsatzart_id, kategorie_id, ort_id, wertstellung, einnahmen, ausgaben from cl_transactions;'
r_sql_query = 'select umsatzart_id, umsatzart from cl_revenue_types;'
o_sql_query = 'select ort_id, stadt from cl_places;'
c_sql_query = 'select kategorie_id, kategorie, haendler, beguenstigterauftraggeber from cl_categories;'

t_df = hb.read_sql(haushaltsbuch_db, t_sql_query)
r_df = hb.read_sql(haushaltsbuch_db, r_sql_query)
o_df = hb.read_sql(haushaltsbuch_db, o_sql_query)
c_df = hb.read_sql(haushaltsbuch_db, c_sql_query)

#-----------------------------------------------------------------------
# DATA MART: Modify data
#-----------------------------------------------------------------------
t_df['Bilanz'] = 'TBD'
for index, row in t_df.iterrows():
    if row['Ausgaben'] < 0.0:
        t_df.set_value(index,'Bilanz',row['Ausgaben'])
    elif row['Einnahmen'] > 0:
        t_df.set_value(index,'Bilanz',row['Einnahmen'])

t_df.loc[:,'Ausgaben'] *= -1

dummy_df = pd.merge(left=t_df, right=r_df, on='Umsatzart_ID', how='left')
dummy_df_2 = pd.merge(left=dummy_df, right=o_df, on='Ort_ID', how='left')
data_mart_df = pd.merge(left=dummy_df_2, right=c_df, on='Kategorie_ID', how='inner')

val_normalize = hb.read_normalize_value()
data_mart_tableau = data_mart_df.copy()

hb.normalize_data(data_mart_tableau, 'Ausgaben', val_normalize)
hb.normalize_data(data_mart_tableau, 'Einnahmen', val_normalize)
hb.normalize_data(data_mart_tableau, 'Bilanz', val_normalize)

#-----------------------------------------------------------------------
# DATA MART: Load table
#-----------------------------------------------------------------------
hb.load_table(data_mart_df, 'data_mart', haushaltsbuch_db, 'replace')
hb.save_csv(data_mart_df, '/Users/Potzenhotz/data/final_data/data_mart.csv', ';')
hb.save_csv(data_mart_tableau, '/Users/Potzenhotz/data/final_data/data_mart_tableau.csv', ';')


