#!/bin/env python3
'''
Data Mart Layer
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


