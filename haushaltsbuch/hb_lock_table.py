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

class Gatekeeper(Base):
    __tablename__ = 'cl_gatekeeper'

    id = Column(Integer, Sequence('gatekeeper_id_seq'), primary_key=True)
    lock_start = Column(DateTime)
    lock_end = Column(DateTime)
    insert_ts = Column(DateTime, default=func.now())
    #insert_ts = Column(DateTime, default=datetime.datetime.utcnow())

#-----------------------------------------------------------------------
#Create Table
#-----------------------------------------------------------------------
logger.info('Following table will be created: {}'.format(Gatekeeper.__table__))

Base.metadata.create_all(haushaltsbuch_db)
