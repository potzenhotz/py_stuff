#!/bin/env python3

#-----------------------------------------------------------------------
# Modules for import
#-----------------------------------------------------------------------
import pandas as pd
from sqlalchemy import create_engine, text
import sys
import csv
import numpy as np
import hb_functions as hb
import lm_logging as lml
import datetime

pd.options.display.max_colwidth = 170

#-----------------------------------------------------------------------
# Logging
#-----------------------------------------------------------------------
log = lml.simple_logging()
#log.set_logfile()
log.set_console()
logger = log.rootLogger
#logger.setLevel(log.logging.ERROR)
logger.setLevel(log.logging.INFO)
#logger.setLevel(log.logging.DEBUG)


#-----------------------------------------------------------------------
#Define database
#-----------------------------------------------------------------------
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')


#-----------------------------------------------------------------------
#Read core
#-----------------------------------------------------------------------
logger.info('Start reading core layer')
sql_q_core = 'select * from cl_DeuBa;'
loaded_core_df = pd.read_sql_query(sql_q_core, haushaltsbuch_db)
if loaded_core_df.empty:
    logger.error('No data in staging layer')
    sys.exit()

#-----------------------------------------------------------------------
#Merge all rows to one long string
#-----------------------------------------------------------------------
loaded_core_df = loaded_core_df.replace(np.nan, '', regex=True)
merged_core_df = pd.DataFrame(columns=['merged'])
counter = 0
for column in loaded_core_df:
    if counter == 0:
        merged_core_df['merged'] = loaded_core_df[column] + ' '
    else:
        if column == 'soll' or column == 'haben':
            merged_core_df['merged'] = merged_core_df['merged'] + loaded_core_df[column].map(str) + ' '
        else:
            merged_core_df['merged'] = merged_core_df['merged'] + loaded_core_df[column] + ' '
    counter += 1
merged_core_df['merged'] = merged_core_df['merged'].str.upper()
logger.debug(merged_core_df.head())


# rules table = num_rule, search_str_1, search_str_2 ...
# num_rule repraesentiert kategorie, welche dann auf konsumkategorie schliesst
# itter durch rows
#   itter durch die colums
#       wenn ein column trifft counter hoch setzen
#   rule setzen und counter anzahl speichern
#   wenn neue rule hoeheren counter hat austauschen...
for ind_merged, row_merged in merged_core_df.iterrows():
    for idx_rules, row_rules in dm_rules_df.iterrows():
        rule_hit_counter = 0
        current_rule = row_rules['kategorie']
        for column_rules in dm_rules_df:
            if column_rules != 'kategorie':
            if row_rules[column_rules] in row_merged['merged']:
                rule_hit_counter += 1
        if current_rule_hit_counter < rule_hit_counter:
            current_rule = row_rules['kategorie']
            current_rule_hit_counter = rule_hit_counter
        
    #print(row['merged'].str.contains('ALDI'))
#print(merged_core_df[merged_core_df['merged'].str.contains("ALDI")])
#-----------------------------------------------------------------------
# Load table
#-----------------------------------------------------------------------
logger.info('Loading core layer')
#core_df = loaded_staging_df.loc[loaded_staging_df['already_loaded'] == 0]
#hb.load_table(core_df, 'cl_deuBa', haushaltsbuch_db, 'append')



