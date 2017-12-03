#!/bin/env python3

#-----------------------------------------------------------------------
# Modules for import
#-----------------------------------------------------------------------
import datetime
import lm_logging as lml
from sqlalchemy import create_engine # database connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Sequence
from sqlalchemy.sql import func


#-----------------------------------------------------------------------
# Logging
#-----------------------------------------------------------------------
log = lml.simple_logging()
#log.set_logfile()
log.set_console()
logger = log.rootLogger
#logger.setLevel(log.logging.ERROR)
#logger.setLevel(log.logging.INFO)
logger.setLevel(log.logging.DEBUG)


#-----------------------------------------------------------------------
#Define database
#-----------------------------------------------------------------------
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')


#-----------------------------------------------------------------------
#Define Table
#-----------------------------------------------------------------------
Base = declarative_base()

class Rules(Base):
    __tablename__ = 'dm_rules'

    id = Column(Integer, Sequence('rules_id_seq'), primary_key=True)
    kategorie = Column(String)
    unterkategorie = Column(String)
    suchkriterium_1 = Column(String)
    suchkriterium_2 = Column(String)
    suchkriterium_3 = Column(String)
    suchkriterium_4 = Column(String)
    suchkriterium_5 = Column(String)
    insert_ts = Column(DateTime, default=datetime.datetime.utcnow())

#-----------------------------------------------------------------------
#Create Table
#-----------------------------------------------------------------------
logger.info('Following table will be created: {}'.format(Rules.__table__))

Base.metadata.create_all(haushaltsbuch_db)
