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
Drop Tables
'''
connection = haushaltsbuch_db.raw_connection()
cursor = connection.cursor()
command = "DROP TABLE IF EXISTS ht_uebersetzung;"
cursor.execute(command)
command = "DROP TABLE IF EXISTS ht_staedte;"
cursor.execute(command)
command = "DROP TABLE IF EXISTS ht_auftraggeber;"
cursor.execute(command)
connection.commit()
cursor.close()

'''
Help Tables
'''
metadata = MetaData()
uebersetzung = Table('ht_uebersetzung', metadata,
    Column('id', Integer, primary_key=True),
    Column('raw_value', String),
    Column('uebersetzung', String)
)

staedte = Table('ht_staedte', metadata,
    Column('id', Integer, primary_key=True),
    Column('raw_value', String),
    Column('stadt', String)
)

auftraggeber = Table('ht_auftraggeber', metadata,
    Column('id', Integer, primary_key=True),
    Column('raw_value', String),
    Column('auftraggeber', String)
)
metadata.create_all(haushaltsbuch_db)
'''
Insert into tables
'''
conn = haushaltsbuch_db.connect()
ins = uebersetzung.insert()
conn.execute(ins, raw_value='KREDITKARTE', uebersetzung='Kreditkarte')
conn.execute(ins, raw_value='Miete Lukas Lübeck', uebersetzung='Miete')
conn.execute(ins, raw_value='Miete Lukas', uebersetzung='Miete')
conn.execute(ins, raw_value='monatliche Sparrate', uebersetzung='ETF-Sparplan')
conn.execute(ins, raw_value='Wertpapiersparplan', uebersetzung='ETF-Sparplan')
conn.execute(ins, raw_value='Sparbuch', uebersetzung='Sparbuch')
conn.execute(ins, raw_value='Auxmoney', uebersetzung='Auxmoney')
conn.execute(ins, raw_value='Miete und Co', uebersetzung='Miete')
conn.execute(ins, raw_value='Monatliche Einzahlung', uebersetzung='Miete')
conn.execute(ins, raw_value='Sparen', uebersetzung='Sparbuch')
conn.execute(ins, raw_value='Aktien', uebersetzung='Aktien')
conn.execute(ins, raw_value='Akiten', uebersetzung='Aktien')


conn = haushaltsbuch_db.connect()
ins = staedte.insert()
conn.execute(ins, raw_value='Karlsruhe', stadt='Karlsruhe')
conn.execute(ins, raw_value='Dortmund Kley', stadt='Dortmund')
conn.execute(ins, raw_value='LUEBECK', stadt='Luebeck')
conn.execute(ins, raw_value='DORTMUND', stadt='Dortmund')
conn.execute(ins, raw_value='Dortmund', stadt='Dortmund')
conn.execute(ins, raw_value='KASSEL', stadt='Kassel')
conn.execute(ins, raw_value='SANDESNEBEN', stadt='Sandesneben')
conn.execute(ins, raw_value='Luebeck', stadt='Luebeck')
conn.execute(ins, raw_value='Lübeck', stadt='Luebeck')
conn.execute(ins, raw_value='QUARTU SANT', stadt='Cagliari')
conn.execute(ins, raw_value='VILLAISMIUS', stadt='Cagliari')
conn.execute(ins, raw_value='CAGLIARI', stadt='Cagliari')
conn.execute(ins, raw_value='Hamburg', stadt='Hamburg')
conn.execute(ins, raw_value='BOCHUM', stadt='Bochum')
conn.execute(ins, raw_value='Luxembourg', stadt='Luxembourg')
conn.execute(ins, raw_value='HH-AIRPORT', stadt='Hamburg')
conn.execute(ins, raw_value='HAMBURG', stadt='Hamburg')
conn.execute(ins, raw_value='GOTEBORG', stadt='Gothenburg')
conn.execute(ins, raw_value='HH-SEEBURG', stadt='Hamburg')

conn = haushaltsbuch_db.connect()
ins = auftraggeber.insert()
conn.execute(ins, raw_value='HM', auftraggeber='H+M')
conn.execute(ins, raw_value='PEEK+CLOPPENBURG', auftraggeber='P+C')
conn.execute(ins, raw_value='PEEK + CLOPPENBURG', auftraggeber='P+C')
conn.execute(ins, raw_value='Jonas Pasche', auftraggeber='UEBERSPACE')
conn.execute(ins, raw_value='LUISE', auftraggeber='OMA')
conn.execute(ins, raw_value='DESK SERVICES', auftraggeber='HONOR 8')
conn.execute(ins, raw_value='MEDIA MAR', auftraggeber='MEDIA MARKT')


