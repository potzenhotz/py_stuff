#!/bin/env python3
'''
Core Layer
'''

########################################################################
# Modules for import
########################################################################
import pandas as pd
import numpy as np
from sqlalchemy import create_engine # database connection

########################################################################
# Functions
########################################################################

def read_sql(database, sql_query):
    df = pd.read_sql_query(sql_query, database)
    return df

def read_normalize_value():
    with open('/Users/Potzenhotz/data/raw_data/normalize.txt', 'r') as f:
        read_data = f.read()
    f.closed
    val_normalize = int(read_data)
    return val_normalize

def normalize_data(df, field, val_normalize):
    df.loc[:,field] /= val_normalize

def load_table(df, table_name, database, load_type):
    df.to_sql(table_name, database, if_exists=load_type, index=False)

def save_csv(df, file_path, seperator):
    df.to_csv(file_path, sep=seperator, index=False)
 
########################################################################
# Load Database into dataframe
########################################################################
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')

il_sql_query = 'select ,wertstellung, umsatzart, beguenstigterauftraggeber, verwendungszweck
                        , iban, bic, soll, haben, währung from integration_layer;'

il_df = read_sql(haushaltsbuch_db, il_sql_query)


#Create Keys for certain rows
il_df['Kategorie_ID'] = pd.factorize(il_df.BeguenstigterAuftraggeber)[0]
il_df['Umsatzart_ID'] = pd.factorize(il_df.Umsatzart)[0]

transaction_df = il_df[['Umsatzart_ID', 'Kategorie_ID'
                        , 'Soll', 'Haben', 'Wertstellung']].copy()
revenue_type_df = il_df[['Umsatzart_ID','Umsatzart']].copy()
category_df = il_df[['Kategorie_ID','BeguenstigterAuftraggeber']].copy()

category_df.drop_duplicates(inplace=True)
revenue_type_df.drop_duplicates(inplace=True)
category_df['Kategorie'] = 'no_data'
category_df['Haendler'] = 'no_data'

########################################################################
# Define categories
########################################################################
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

########################################################################
# Modify rows and columns
########################################################################
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

########################################################################
# Load core layer database
########################################################################
load_table(transaction_df, 'cl_transactions', haushaltsbuch_db, 'replace')
load_table(revenue_type_df, 'cl_revenue_types', haushaltsbuch_db, 'replace')
load_table(category_df, 'cl_categories', haushaltsbuch_db, 'replace')



########################################################################
# Load Database into dataframe
########################################################################
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')
t_sql_query = 'select umsatzart_id, kategorie_id, wertstellung, einnahmen, ausgaben from cl_transactions;'
r_sql_query = 'select umsatzart_id, umsatzart from cl_revenue_types;'
c_sql_query = 'select kategorie_id, kategorie, haendler, beguenstigterauftraggeber from cl_categories;'

t_df = read_sql(haushaltsbuch_db, t_sql_query)
r_df = read_sql(haushaltsbuch_db, r_sql_query)
c_df = read_sql(haushaltsbuch_db, c_sql_query)


t_df['Bilanz'] = 'TBD'
for index, row in t_df.iterrows():
    if row['Ausgaben'] < 0.0:
        t_df.set_value(index,'Bilanz',row['Ausgaben'])
    elif row['Einnahmen'] > 0:
        t_df.set_value(index,'Bilanz',row['Einnahmen'])

t_df.loc[:,'Ausgaben'] *= -1


dummy_df = pd.merge(left=t_df ,right=r_df, on='Umsatzart_ID',how='left')
data_mart_df = pd.merge(left=dummy_df ,right=c_df, on='Kategorie_ID',how='inner')

val_normalize = read_normalize_value()
data_mart_tableau = data_mart_df.copy()

normalize_data(data_mart_tableau, 'Ausgaben', val_normalize)
normalize_data(data_mart_tableau, 'Einnahmen', val_normalize)
normalize_data(data_mart_tableau, 'Bilanz', val_normalize)

load_table(data_mart_df, 'data_mart', haushaltsbuch_db, 'replace')
save_csv(data_mart_df, '/Users/Potzenhotz/data/final_data/data_mart.csv', ';')
save_csv(data_mart_tableau, '/Users/Potzenhotz/data/final_data/data_mart_tableau.csv', ';')


