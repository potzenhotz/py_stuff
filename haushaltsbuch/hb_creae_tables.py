#!/bin/env python3
'''
 Modules for import
'''
import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData, ForeignKey
from sqlalchemy import DateTime, Integer, String, Float
'''
Create tables
'''

haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db', echo=True)
'''
Staging
'''
metadata = MetaData()
users = Table('sl_DeuBa', metadata,
    Column('id', Integer, primary_key=True),
    Column('Buchungstag', DateTime),
    Column('Wertstellung', DateTime),
    Column('Umsatzart', String),
    Column('Auftraggeber', String),
    Column('Verwendungszweck', String),
    Column('IBAN', String),
    Column('BIC', String),
    Column('Soll', Float),
    Column('Haben', Float),
    Column('Waehrung', String),
    Column('new_flag', Integer),
)

'''
Core 
'''
konsum_kateogrie = Table('cl_konsum', metadata,
    Column('konsumkategorie_id', Integer, primary_key=True),
    Column('konsumkategorie', String, nullable=False)
)
haendler_kategorie = Table('cl_haendler', metadata,
    Column('haendlerkategorie_id', Integer, primary_key=True),
    Column('konsumkategorie_id', None, ForeignKey('cl_konsum.konsumkategorie_id')),
    Column('haendlerkategorie', String, nullable=False)
)
auftraggeber = Table('cl_auftraggeber', metadata,
    Column('auftraggeber_id', Integer, primary_key=True),
    Column('haendlerkategorie_id', None, ForeignKey('cl_haendler.haendlerkategorie_id')),
    Column('auftraggeber', String, nullable=False),
    Column('IBAN', String),
    Column('BIC', String)
)

ort = Table('cl_ort', metadata,
    Column('ord_id', Integer, primary_key=True),
    Column('stadt', String, nullable=False),
    Column('land', String),
    Column('lat', String),
    Column('lon', String)
)

umsatzart = Table('cl_umsatzart', metadata,
    Column('umsatzart_id', Integer, primary_key=True),
    Column('umsatzart', String, nullable=False)
)


transaktion = Table('cl_transaktion', metadata,
    Column('transaktions_id', Integer, primary_key=True),
    Column('auftraggeber_id', None, ForeignKey('cl_haendler.haendlerkategorie_id')),
    Column('auftraggeber_id', None, ForeignKey('cl_ort.ort_id')),
    Column('auftraggeber_id', None, ForeignKey('cl_umsatzart.umsatzart_id')),
    Column('wertstellung', DateTime, nullable=False),
    Column('verwendungszweck', String, nullable=False),
    Column('soll', Float),
    Column('haben', Float)
)



metadata.create_all(haushaltsbuch_db)
'''
Insert into tables
'''
"""
ins = users.insert().values(name='lukas', fullname='Lukas Muessle')
print(str(ins))
print(ins.compile().params  )


conn = haushaltsbuch_db.connect()
result = conn.execute(ins)
"""
