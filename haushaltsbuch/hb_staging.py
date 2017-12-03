#!/bin/env python3

#-----------------------------------------------------------------------
# Modules for import
#-----------------------------------------------------------------------
import pandas as pd
from sqlalchemy import create_engine # database connection
import sys
import csv
import hb_functions as hb
import lm_logging as lml


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
#Define input parameters
#-----------------------------------------------------------------------
logger.info('Reading parameters')
input_arguments = sys.argv
file_name = sys.argv[1]
logger.debug('Following parameters are loaded:{}'.format(input_arguments))


#-----------------------------------------------------------------------
#Define database
#-----------------------------------------------------------------------
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')


#-----------------------------------------------------------------------
#STAGING: Read csv
#-----------------------------------------------------------------------
logger.info('Reading csv {}'.format(file_name))
staging_df = pd.read_csv(file_name, encoding="ISO-8859-1", sep=';', skiprows=4, skipfooter=1, engine='python')
logger.debug('Following columns are loeaded from csv: {}'.format(list(staging_df)))
logger.debug('Following head from csv: {}'.format(staging_df.head()))

#-----------------------------------------------------------------------
#STAGING: Clean data
#-----------------------------------------------------------------------
logger.info('Cleaning data')
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

staging_df['soll'] = staging_df['soll'].str.replace('.', '')
staging_df['soll'] = staging_df['soll'].str.replace(',', '.')
staging_df['soll'] = staging_df['soll'].astype(float)

staging_df['haben'] = staging_df['haben'].str.replace('.', '')
staging_df['haben'] = staging_df['haben'].str.replace(',', '.')
staging_df['haben'] = staging_df['haben'].astype(float)

staging_df['wertstellung'] =  pd.to_datetime(staging_df['wertstellung'], format='%d.%m.%Y')
staging_df['buchungstag'] =  pd.to_datetime(staging_df['buchungstag'], format='%d.%m.%Y')
 
logger.debug('Data Types for loading: {}'.format(staging_df.dtypes))
#-----------------------------------------------------------------------
# STAGING: Load table
#-----------------------------------------------------------------------
logger.info('Loading staging layer')
hb.load_table(staging_df, 'sl_DeuBa', haushaltsbuch_db, 'replace')


