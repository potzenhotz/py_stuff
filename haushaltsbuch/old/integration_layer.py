#!/bin/env python3
'''
Integration Layer
'''

########################################################################
# Modules for import
########################################################################
import pandas as pd
import numpy as np
from sqlalchemy import create_engine # database connection

#par_load='initial'
par_load='append'

########################################################################
# Funcations
########################################################################
def clean_df_db_dups(df, tablename, engine, dup_cols=[],
                         filter_continuous_col=None, filter_categorical_col=None):
    """
    Remove rows from a dataframe that already exist in a database
    Required:
        df : dataframe to remove duplicate rows from
        engine: SQLAlchemy engine object
        tablename: tablename to check duplicates in
        dup_cols: list or tuple of column names to check for duplicate row values
    Optional:
        filter_continuous_col: the name of the continuous data column for BETWEEEN min/max filter
                               can be either a datetime, int, or float data type
                               useful for restricting the database table size to check
        filter_categorical_col : the name of the categorical data column for Where = value check
                                 Creates an "IN ()" check on the unique values in this column
    Returns
        Unique list of values from dataframe compared to database table
    """
    args = 'SELECT %s FROM %s' %(', '.join(['"{0}"'.format(col) for col in dup_cols]), tablename)
    args_contin_filter, args_cat_filter = None, None
    if filter_continuous_col is not None:
        if df[filter_continuous_col].dtype == 'datetime64[ns]':
            args_contin_filter = """ "%s" BETWEEN Convert(datetime, '%s')
                                          AND Convert(datetime, '%s')""" %(filter_continuous_col,
                              df[filter_continuous_col].min(), df[filter_continuous_col].max())


    if filter_categorical_col is not None:
        args_cat_filter = ' "%s" in(%s)' %(filter_categorical_col,
                          ', '.join(["'{0}'".format(value) for value in df[filter_categorical_col].unique()]))

    if args_contin_filter and args_cat_filter:
        args += ' Where ' + args_contin_filter + ' AND' + args_cat_filter
    elif args_contin_filter:
        args += ' Where ' + args_contin_filter
    elif args_cat_filter:
        args += ' Where ' + args_cat_filter

    df.drop_duplicates(dup_cols, keep='last', inplace=True)
    df = pd.merge(df, pd.read_sql(args, engine), how='left', on=dup_cols, indicator=True)
    df = df[df['_merge'] == 'left_only']
    df.drop(['_merge'], axis=1, inplace=True)
    return df
########################################################################
# Load Database into dataframe
########################################################################
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')

#integration layer
raw_il_df = pd.read_sql_query('select buchungstag\
                                     , wertstellung\
                                     , umsatzart\
                                     , beguenstigterauftraggeber\
                                     , verwendungszweck\
                                     , iban\
                                     , bic\
                                     , soll\
                                     , haben\
                                     , währung\
                                     from staging_layer;', haushaltsbuch_db)


########################################################################
# Some tests
########################################################################

#print(raw_il_df.iloc[1])
#raw_il_df.replace('no data', np.NaN, inplace=True)
#print(raw_il_df.dtypes)

########################################################################
# Modify rows and columns
########################################################################
#ACHTUNG CHANGES WERDEN ERST NACH DEM LOOP COMMITED
#DAHER REIHENFOLGE WICHTIG
for index, row in raw_il_df.iterrows():
    if pd.isnull(row['BeguenstigterAuftraggeber']):
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber', row['Verwendungszweck'].split('/')[0])

    if row['Verwendungszweck'].find('KREDITKARTE') != -1:
        raw_il_df.set_value(index,'Umsatzart','Kreditkarte')
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','Kreditkarte')

    if row['Verwendungszweck'].find('Miete Lukas Lübeck') != -1:
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','Miete')

    if row['Verwendungszweck'].find('monatliche Sparrate') != -1:
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','ETF-Sparplan')

    if row['Verwendungszweck'].find('Sparbuch') != -1:
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','Sparbuch')

    if row['Verwendungszweck'].find('Auxmoney') != -1:
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','Auxmoney')

    if row['Verwendungszweck'].find('Miete und Co') != -1:
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','Miete')

    if row['Verwendungszweck'].find('Monatliche Einzahlung') != -1:
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','Miete')

    if row['Verwendungszweck'].find('Sparen') != -1:
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','Sparbuch')

    if row['Verwendungszweck'].find('Aktien') != -1:
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','Aktien')

    if row['Verwendungszweck'].find('Akiten') != -1:
        raw_il_df.set_value(index,'BeguenstigterAuftraggeber','Aktien')

    if row['Umsatzart'] is not None:
        if row['Umsatzart'].find('Auszahlung Geldautomat') != -1:
            raw_il_df.set_value(index,'BeguenstigterAuftraggeber', 'Auszahlung Geldautomat')
'''
########################################################################
# Add index
########################################################################
raw_il_df['ID'] = raw_il_df.index

########################################################################
# Rearange columns
########################################################################
cols = raw_il_df.columns.tolist()
#cols[-1:] last column
#cols[:-1] all columns except last
cols = cols[-1:] + cols[:-1]
raw_il_df = raw_il_df[cols]
'''
########################################################################
# Load core layer database
########################################################################

if par_load == 'initial':
    il_df = raw_il_df
elif par_load == 'append':
    columns = ['Wertstellung', 'Verwendungszweck']
    il_df = clean_df_db_dups(raw_il_df, 'integration_layer', haushaltsbuch_db, columns) 

il_df.to_sql('integration_layer', haushaltsbuch_db, if_exists='append', index=False)
