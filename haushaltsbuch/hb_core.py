#!/bin/env python3

'''
-----------------------------------------------------------------------
 Modules for import
-----------------------------------------------------------------------
'''
import pandas as pd
from sqlalchemy import create_engine, MetaData 
import sys
import csv
import numpy as np
import hb_functions as hb

'''
#-----------------------------------------------------------------------
#Define database
#-----------------------------------------------------------------------
'''
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')

'''
-----------------------------------------------------------------------
 CORE: Read table
-----------------------------------------------------------------------
'''
print('Start reading tables')
staging_sql_query = 'select sl_id, wertstellung, umsatzart, auftraggeber \
                , stadt, verwendungszweck, iban, bic, soll, haben, new_flag from sl_DeuBa \
                where new_flag = 1;'
loaded_staging_df = hb.read_sql(haushaltsbuch_db, staging_sql_query)
if loaded_staging_df.empty:
    print('All rows from staging layer are already in core')
    print('EXIT CODE')
    sys.exit()

auftraggeber_sql_query = 'select auftraggeber_id, auftraggeber from cl_auftraggeber'
auftraggeber_df = hb.read_sql(haushaltsbuch_db, auftraggeber_sql_query)

umsatzart_sql_query = 'select umsatzart_id, umsatzart from cl_umsatzart'
umsatzart_df = hb.read_sql(haushaltsbuch_db, umsatzart_sql_query)

ort_sql_query = 'select ort_id, stadt from cl_ort'
ort_df = hb.read_sql(haushaltsbuch_db, ort_sql_query)

metadata = MetaData(haushaltsbuch_db, reflect=True)
sl_DeuBa = metadata.tables['sl_DeuBa']
'''
-----------------------------------------------------------------------
 CORE: Modify rows and columns
-----------------------------------------------------------------------
'''
print('Start modifing rows and columns')

flag_auftraggeber = 0
flag_ort = 0
flag_umsatzart = 0
transaktion_df = pd.DataFrame(columns=['wertstellung'\
                                        , 'auftraggeber_id'\
                                        , 'ort_id'\
                                        , 'umsatzart_id'\
                                        , 'soll'\
                                        , 'haben'\
                                        ])

print('Start itterrows')
for index, row in loaded_staging_df.iterrows():
    flag_auftraggeber = 0
    flag_ort = 0
    flag_umsatzart = 0
    for lkp_index, lkp_row in auftraggeber_df.iterrows():
            if row['auftraggeber'].upper().find(lkp_row['auftraggeber'].upper()) != -1:
                buffer_auftraggeber_id = lkp_row['auftraggeber_id']
                flag_auftraggeber = 1
            else:
                del_index_auftraggeber = index
    for lkp_index, lkp_row in ort_df.iterrows():
        if not row['stadt']:
            flag_ort=2
        else:
            if row['stadt'].upper().find(lkp_row['stadt'].upper()) != -1:
                buffer_ort_id = lkp_row['ort_id']
                flag_ort = 1
            else:
                del_index_ort = index
    for lkp_index, lkp_row in umsatzart_df.iterrows():
        if not row['umsatzart']:
            flag_umsatzart=2
        else:
            if row['umsatzart'].upper().find(lkp_row['umsatzart'].upper()) != -1:
                buffer_umsatzart_id = lkp_row['umsatzart_id']
                flag_umsatzart = 1
            else:
                del_index_umsatzart = index

    if flag_auftraggeber == 1 \
        and (flag_ort == 1 or flag_ort == 2)\
        and (flag_umsatzart == 1 or flag_umsatzart ==2) :
            to_df_auftraggeber_id = buffer_auftraggeber_id 
            if flag_ort == 2:
                to_df_ort_id = -1
            else:
                to_df_ort_id = buffer_ort_id
            if flag_umsatzart == 2:
                to_df_umsatzart_id = -1
            else:
                to_df_umsatzart_id = buffer_umsatzart_id 
            to_df_wertstellung = row['wertstellung']
            to_df_soll = row['soll']
            to_df_haben = row['haben']
            transaktion_df = transaktion_df.append(pd.Series([to_df_wertstellung\
                                                , to_df_auftraggeber_id\
                                                , to_df_ort_id\
                                                , to_df_umsatzart_id\
                                                , to_df_soll\
                                                , to_df_haben\
                                                ]\
                                                , index=['wertstellung'\
                                                ,'auftraggeber_id'\
                                                ,'ort_id'\
                                                ,'umsatzart_id'\
                                                ,'soll'\
                                                ,'haben'\
                                                ]), ignore_index=True)
            update_stmt = sl_DeuBa.update().where(sl_DeuBa.c.sl_id == row['sl_id']).values(new_flag=0)
            conn = haushaltsbuch_db.connect()
            conn.execute(update_stmt)
    else:
        print('#----------------------------------------------------#')
        print('Following row could not be loaded \n and will be deleted in stage')
        print(row['verwendungszweck'])
        if flag_auftraggeber == 0:
            print('Auftraggeber nicht gefunden', row['auftraggeber'])
        elif flag_ort == 0:
            print('Ort nicht gefunden', row['stadt'])
        elif flag_umsatzart == 0:
            print('Umsatzart nicht gefunden', row['umsatzart'])
        delete_stmt = sl_DeuBa.delete().where(sl_DeuBa.c.sl_id == row['sl_id'])
        conn = haushaltsbuch_db.connect()
        conn.execute(delete_stmt)
        
'''
-----------------------------------------------------------------------
 CORE: drop columns
-----------------------------------------------------------------------
'''
#0 for rows and 1 for columns


'''
-----------------------------------------------------------------------
 CORE: Load table
-----------------------------------------------------------------------
'''
#print(list(transaktion_df))
#print(transaktion_df.head())
hb.load_table(transaktion_df, 'cl_transaktion', haushaltsbuch_db, 'append')

'''

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

'''
