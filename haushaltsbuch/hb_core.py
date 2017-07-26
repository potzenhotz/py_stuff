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
 CORE: Load table
-----------------------------------------------------------------------
'''
#print(list(transaktion_df))
#print(transaktion_df.head())
hb.load_table(transaktion_df, 'cl_transaktion', haushaltsbuch_db, 'append')

