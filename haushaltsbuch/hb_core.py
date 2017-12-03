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
#Read Staging
#-----------------------------------------------------------------------
logger.info('Start reading staging layer')
dates_staging = ['wertstellung', 'buchungstag']
sql_q_staging = 'select * from sl_DeuBa;'
loaded_staging_df = pd.read_sql_query(sql_q_staging, haushaltsbuch_db, parse_dates=dates_staging)
if loaded_staging_df.empty:
    logger.info('No data in staging layer')
    sys.exit()

loaded_staging_df['already_loaded'] = 0

min_date = loaded_staging_df.wertstellung.min()
max_date = loaded_staging_df.wertstellung.max()

logger.debug('Min date from staging layer {}'.format(min_date))
logger.debug('Max date from staging layer {}'.format(max_date))

dates_gatekeeper = ['lock_end', 'lock_start']
sql_q_gatekeeper = 'select lock_start, lock_end from cl_gatekeeper;'
gatekeeper_df = pd.read_sql_query(sql_q_gatekeeper, haushaltsbuch_db, parse_dates=dates_gatekeeper)

if gatekeeper_df.empty:
    logger.info('All rows will be loaded')
else:
    counter_loaded = 0
    counter_to_load = 0
    for index, row in loaded_staging_df.iterrows():
        for g_index, g_row in gatekeeper_df.iterrows():
            if g_row['lock_start'] <= row['wertstellung'] <= g_row['lock_end']:
                logger.debug("Date in between {0} {1}: {2}".format(g_row['lock_start'], g_row['lock_end'],row['wertstellung']))
                loaded_staging_df.set_value(index, 'already_loaded', 1)
                counter_loaded += 1
            else:
                logger.debug("Date NOT in {0} {1}: {2}".format(g_row['lock_start'], g_row['lock_end'],row['wertstellung']))
                counter_to_load += 1

    logger.info('{} rows are already in core layer'.format(counter_loaded))
    logger.info('{} rows will be loaded'.format(counter_to_load))

#-----------------------------------------------------------------------
# Insert into lock table
#-----------------------------------------------------------------------
str_sql_1 = 'insert into cl_gatekeeper (lock_start, lock_end, insert_ts) VALUES '
str_sql_2 = '(\'{0}\', \'{1}\', \'{2}\');'.format(str(min_date),str(max_date),str(datetime.datetime.now()))
sql = text(str_sql_1 + str_sql_2)
logger.info('Following SQL is executed: {}'.format(sql))
result = haushaltsbuch_db.engine.execute(sql)

#-----------------------------------------------------------------------
# Load table
#-----------------------------------------------------------------------
logger.info('Loading core layer')
core_df = loaded_staging_df.loc[loaded_staging_df['already_loaded'] == 0]
core_df.pop('already_loaded')
hb.load_table(core_df, 'cl_deuBa', haushaltsbuch_db, 'append')



