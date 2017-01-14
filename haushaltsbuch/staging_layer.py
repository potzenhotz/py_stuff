#!/bin/env python3
'''
Staging Layer
'''
import pandas as pd
from sqlalchemy import create_engine # database connection


disk_engine = create_engine('sqlite:///staging_layer.db')

file_name = 'raw_data/Kontoumsaetze_350_355327800_20170114_175539.csv'

df = pd.read_csv(file_name, encoding = "ISO-8859-1", sep=';', skiprows=4 )

df.to_sql('staging_layer', disk_engine, if_exists='replace')

#staging_layer_df = pd.read_sql_query('SELECT * FROM data LIMIT 3', disk_engine)
