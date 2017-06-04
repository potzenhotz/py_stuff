#!/bin/env python3
'''
 Modules for import
'''
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
'''
Create tables
'''

haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db', echo=True)

metadata = MetaData()
users = Table('test_users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
)

addresses = Table('test_addresses', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', None, ForeignKey('test_users.id')),
    Column('email_address', String, nullable=False)
)


metadata.create_all(haushaltsbuch_db)
'''
Insert into tables
'''
ins = users.insert().values(name='lukas', fullname='Lukas Muessle')
print(str(ins))
print(ins.compile().params  )


conn = haushaltsbuch_db.connect()
result = conn.execute(ins)
