#!/bin/env python3

import pandas as pd
########################################################################
# Funcations
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

def load_table(df, table_name, database, load_type, index_type=False):
    df.to_sql(table_name, database, if_exists=load_type, index=index_type)

def save_csv(df, file_path, seperator):
    df.to_csv(file_path, sep=seperator, index=False)

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

