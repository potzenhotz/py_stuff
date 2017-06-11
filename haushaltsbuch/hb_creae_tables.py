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
    Column('sl_id', Integer, primary_key=True),
    Column('buchungstag', DateTime),
    Column('wertstellung', DateTime),
    Column('umsatzart', String),
    Column('auftraggeber', String),
    Column('stadt', String),
    Column('land', String),
    Column('verwendungszweck', String),
    Column('IBAN', String),
    Column('BIC', String),
    Column('soll', Float),
    Column('haben', Float),
    Column('waehrung', String),
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
    Column('ort_id', Integer, primary_key=True),
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
    Column('wertstellung', DateTime, nullable=False),
    Column('auftraggeber_id', None, ForeignKey('cl_haendler.haendlerkategorie_id')),
    Column('ort_id', None, ForeignKey('cl_ort.ort_id')),
    Column('umsatzart_id', None, ForeignKey('cl_umsatzart.umsatzart_id')),
    Column('soll', Float),
    Column('haben', Float),
)

#mart_konsum = Table('dm_konsum', metadata,
#    Column('dm_konsum_id', Integer, primary_key=True),
#    Column('monat', String, nullable=False),
#    Column('konsumkategorie', String, nullable=False),
#    Column('soll', Float )
#)


metadata.create_all(haushaltsbuch_db)
