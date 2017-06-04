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

#-----------------------------------------------------------------------
# CORE: Read table
#-----------------------------------------------------------------------
staging_sql_query = 'select wertstellung, umsatzart, auftraggeber\
                , verwendungszweck, iban, bic, soll, haben from sl_DeuBa \
                where new_flag = 1;'

loaded_staging_df = hb.read_sql(haushaltsbuch_db, staging_sql_query)

#-----------------------------------------------------------------------
# CORE: Modify rows and columns
#-----------------------------------------------------------------------
#ACHTUNG CHANGES WERDEN ERST NACH DEM LOOP COMMITED
#DAHER REIHENFOLGE WICHTIG
uebersetzung = {'KREDITKARTE': 'Kreditkarte','Miete Lukas Lübeck': 'Miete'
                , 'monatliche Sparrate':'ETF-Sparplan', 'Sparbuch': 'Sparbuch', 'Auxmoney':'Auxmoney'
                , 'Miete und Co': 'Miete', 'Monatliche Einzahlung':'Miete', 'Sparen':'Sparbuch'
                , 'Aktien':'Aktien', 'Akiten':'Aktien'}

staedte = {'KARLSRUHE':'Karlsruhe', 'Dortmund Kley':'Dortmund', 'LUEBECK':'Luebeck'
        ,'DORTMUND':'Dortmund','Dortmund':'Dortmund', 'KASSEL':'Kassel', 'SANDESNEBEN':'Sandesneben'
        , 'Luebeck':'Luebeck', 'Lübeck':'Luebeck','QUARTU SANT':'Cagliari', 'VILLASIMIUS':'Cagliari'
        , 'CAGLIARI':'Cagliari', 'Hamburg':'Hamburg', 'BOCHUM':'Bochum', 'Luxembourg':'Luxembourg'
        , 'HH-AIRPORT':'Hamburg', 'HAMBURG':'Hamburg', 'GOTEBORG':'Gothenburg', 'HH-SEEBURG':'Hamburg'
        ,}


uebersetzung_sql_query = 'select raw_value, uebersetzung from ht_uebersetzung' 
uebersetzung_df = hb.read_sql(haushaltsbuch_db, uebersetzung_sql_query)
print(list(uebersetzung_df))


staedte_sql_query = 'select raw_value, stadt from ht_staedte' 
staedte_df = hb.read_sql(haushaltsbuch_db, staedte_sql_query)
print(list(staedte_df))


loaded_staging_df['Stadt'] = None
loaded_staging_df['Land'] = 'no_data'

for index, row in loaded_staging_df.iterrows():
    if pd.isnull(row['Auftraggeber']):
        loaded_staging_df.set_value(index,'Auftraggeber', row['Verwendungszweck'].split('/')[0])

    length_verw=len(row['Verwendungszweck'].split('/'))
    #print(length_verw)
    if length_verw > 2:
        for s_index, s_row in staedte_df.iterrows():
            if row['Verwendungszweck'].split('/')[2].find(s_row['raw_value']) !=-1:
                loaded_staging_df.set_value(index,'Stadt', s_row['stadt'])
                #print(row['Verwendungszweck'].split('/')[2], key, value, index)
                break
    elif length_verw == 2:
        for s_index, s_row in staedte_df.iterrows():
            if row['Verwendungszweck'].split('/')[1].find(s_row['raw_value']) !=-1:
                loaded_staging_df.set_value(index,'Stadt', s_row['stadt'])
                #print('###',row['Verwendungszweck'].split('/')[1], key, value, index)
                break


    for u_index, u_row in uebersetzung_df.iterrows():
        if row['Verwendungszweck'].find(u_row['raw_value']) != -1:
            loaded_staging_df.set_value(index,'Auftraggeber',u_row['uebersetzung'])
            if u_row['raw_value'] == 'KREDITKARTE':
                loaded_staging_df.set_value(index,'Umsatzart',u_row['uebersetzung'])

    if row['Umsatzart'] is not None:
        if row['Umsatzart'].find('Auszahlung Geldautomat') != -1:
            loaded_staging_df.set_value(index,'Auftraggeber', 'Auszahlung Geldautomat')
stop
"""
TODO:
fill dimension tables
fill transaction tables with dimension tables
if not fined in dimension tables do not update staging table
"""


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
places_df['Latitude'] = None
places_df['Longitude'] = None
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
                    , 'Geco':'Lotto', 'KUHN':'Kleidung',}

category_essen = {'METRO':'Einkauf', 'BLAUER ENGEL':'Restautrant', 'WINGAS':'Restaurant', 'REWE':'Einkauf'
                    , 'EDEKA':'Einkauf'
                    , 'AUCHAN':'Einkauf', 'HOLIDAY INN LUEBECK':'Restaurant', 'Jung + Frech':'Restaurant'
                    , 'Vapiano':'Restaurant', 'VAPIANO':'Restaurant'
                    , 'RESTAURANT':'Restaurant', 'famila':'Einkauf', 'SUSHI':'Restaurant'
                    , 'RASTANLAGE':'Restaurant', 'REAL':'Einkauf'
                    , 'Osteria':'Restaurant', 'ALDI':'Einkauf', 'LIDL':'Einkauf', 'Auchan':'Einkauf'
                    , 'SUPERMERCATO':'Einkauf', 'CITTI':'Einkauf', 'LFC LUEBECK':'Restaurant'
                    , 'AKTIV MARKT LUKASIEWICZ':'Einkauf'}

category_haushalt = { 'congstar':'Handy', 'BAUHAUS':'Baumarkt', 'HELLWEG':'Baumarkt'
                    , 'DB Vertrieb':'Mobility'                     
                    , 'BEZIRKSREGIERUNG':'Steuern', 'Miete':'Miete', 'Abschlussposten':'Bank' 
                    , 'DEUTSCHE POST':'Post', 'Jonas Pasche':'Ueberspace'}


category_auto = { 'SHELL':'Tanken', 'SB Tank':'Tanken', 'AVIA':'Tanken', 'OIL TANK':'Tanken'
                    , 'Orlen':'Tanken', 'JET':'Tanken'
                    , 'HDI':'Versicherung', 'BUNDESKASSE IN KIEL':'Steuern', 'Westfalen TS':'Tanken' }

category_firma = { 'Flughafen Hamburg':'Parken', 'Payco Taxi':'Taxi', 'PAYCO':'Taxi'
                    , 'VBK-VERKEHRSBETRIEBE KARLS':'Mobility' }

category_sport = { 'McFIT':'Fitnessstudio', 'FitX':'Fitnessstudio' }

category_sonstiges = { 'TABAK':'Sonstiges' }

category_einnahme = {'NTT':'Gehalt', 'LUISE':'Oma', 'DESK SERVICES':'Honor 8'
                        , 'STEUERVERWALTUNG NRW':'Steuern'}

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

geolocator = geo.Nominatim()
# location could be initialized once into dict to enhance performance in future
for index, row in places_df.iterrows():
    if row['Stadt'] != None:
        location = geolocator.geocode(row['Stadt'])
        places_df.set_value(index,'Latitude',location.latitude)
        places_df.set_value(index,'Longitude',location.longitude)

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
o_sql_query = 'select ort_id, stadt, latitude, longitude from cl_places;'
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


