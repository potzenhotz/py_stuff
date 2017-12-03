#!/bin/env python3
'''
########################################################################
 Modules
########################################################################
'''
import sys
import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData, ForeignKey
from sqlalchemy import DateTime, Integer, String, Float
from sqlalchemy import inspect, text, select
import geopy as geo
import time
'''
########################################################################
Get tables
########################################################################
'''

haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db', echo=True)

# Get table information
inspector = inspect(haushaltsbuch_db)
#print(inspector.get_table_names())

# Create MetaData instance
metadata = MetaData(haushaltsbuch_db, reflect=True)
#print(metadata.tables)

# Get Table
cl_konsum = metadata.tables['cl_konsum']
cl_haendler = metadata.tables['cl_haendler']
cl_auftraggeber = metadata.tables['cl_auftraggeber']
cl_umsatzart = metadata.tables['cl_umsatzart']
cl_ort = metadata.tables['cl_ort']

'''
########################################################################
Truncate tables
########################################################################
'''
connection = haushaltsbuch_db.raw_connection()
cursor = connection.cursor()
command = "DELETE FROM cl_konsum;"
cursor.execute(command)
command = "DELETE FROM cl_haendler;"
cursor.execute(command)
command = "DELETE FROM cl_auftraggeber;"
cursor.execute(command)
command = "DELETE FROM cl_umsatzart;"
cursor.execute(command)
command = "DELETE FROM cl_ort;"
cursor.execute(command)
connection.commit()
cursor.close()


'''
########################################################################
cl_konsum: Insert
########################################################################
'''
conn = haushaltsbuch_db.connect()
ins = cl_konsum.insert()
conn.execute(ins, konsumkategorie='Konsum')
conn.execute(ins, konsumkategorie='Essen')
conn.execute(ins, konsumkategorie='Haushalt')
conn.execute(ins, konsumkategorie='Sport')
conn.execute(ins, konsumkategorie='Firma')
conn.execute(ins, konsumkategorie='Sonstiges')
conn.execute(ins, konsumkategorie='Einnahme')
conn.execute(ins, konsumkategorie='Kreditkarte')
conn.execute(ins, konsumkategorie='Bargeld')
conn.execute(ins, konsumkategorie='Sparen')
conn.execute(ins, konsumkategorie='Urlaub')
conn.execute(ins, konsumkategorie='Alex+Lukas')
conn.execute(ins, konsumkategorie='Auto')


'''
########################################################################
cl_haendler: Insert
########################################################################
Nach zwei bindings muss .connect() aufgerufen werden.
Sonst error:Error binding parameter :x - probably unsupported type.
'''


conn = haushaltsbuch_db.connect()
ins = cl_haendler.insert()
select_stmt = 'SELECT konsumkategorie_id FROM cl_konsum WHERE konsumkategorie=:x'

result = conn.execute(select_stmt, x='Konsum')
row = result.fetchone()
print(row[0])
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Kleidung')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Rimowa')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Rest')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Drogerie')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Buecher')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Elektronik')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Spirituosen')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Schreibwaren')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Amazon')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Paypal')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Lotto')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x='Essen')
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Einkauf')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Restaurant')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Haushalt")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Handy')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Baumarkt')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Mobility')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Steuern')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Bank')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Miete')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Hausrat')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Haushalt Sonstiges')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Sport")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Fitnessstudio')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Sportartikel')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Firma")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Parken')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Taxi')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Firma Mobility')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Sonstiges")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Sonstiges')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Sonstiges Spenden')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Einnahme")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Gehalt')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Einnahmen Sonstiges')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Einnahmen Steuern')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Kreditkarte")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Kreditkarte')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Bargeld")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Auszahlung')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Sparen")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Sparplan')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Sparbuch')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Sonstige Investments')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Urlaub")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Urlaub Sardinien')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Urlaub Ski')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Alex+Lukas")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Gemeinsame Moebel')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='AL Sonstiges')

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x="Auto")
row = result.fetchone()
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Tanken')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Auto Versicherung')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Auto Steuern')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Reparatur')
conn.execute(ins, konsumkategorie_id=row[0], haendlerkategorie='Auto Sonstiges')

'''
########################################################################
cl_auftraggeber: Insert
########################################################################
'''
ins = cl_auftraggeber.insert()
select_stmt = 'SELECT haendlerkategorie_id  FROM cl_haendler WHERE haendlerkategorie=:x'

#KONSUM
list_kleidung = ['P+C', 'H+M', 'TKMAXX', 'KUHN', 'SCHUH BODE', 'FREITAG LAB.', 'PETRA WITT MY HATS']
list_rest = ['RIMOWA','SPOT', 'BVB','ERWIN MATUTT', 'TCHIBO', 'MTB-MARKET GMBH', 'STOWA GmbH'\
            , 'BLUME 2000']
list_drogerie = ['DM', 'DOUGLAS','ROSSMANN']
list_buecher = ['HUGENDUBEL', 'MAYERSCHE', 'PRESSE + BUCH' ]
list_elektronik = ['SATURN', 'MEDIA MARKT']
list_spirituosen = ['WEINHANDLUNG']
list_schreibwaren = ['STAPLES']
list_amazon = ['AMAZON']
list_paypal = ['PAYPAL']
list_lotto = ['GECO']

dict_konsum = {'Kleidung':list_kleidung, 'Rest':list_rest, 'Drogerie':list_drogerie, 'Buecher':list_buecher\
                , 'Elektronik':list_elektronik, 'Spirituosen':list_spirituosen\
                , 'Schreibwaren':list_schreibwaren, 'Amazon':list_amazon\
                , 'Paypal':list_paypal, 'Lotto':list_lotto }

for key, value in dict_konsum.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)


#ESSEN
list_restaurant = ['BLAUER ENGEL', 'WINGAS','HOLIDAY INN LUEBECK', 'JUNG + FRECH', 'VAPIANO'\
                    , 'RESTAURANT', 'SUSHI', 'RASTANLAGE', 'OSTERIA', 'LFC LUEBECK', 'NORDSEE LUEBECK'\
                    , 'NEUE ROESTEREI GMBH', 'PETER PANE', 'NIEDEREGGER'] 
list_einkauf = ['REWE', 'EDEKA', 'METRO', 'AUCHAN', 'FAMILA', 'REAL', 'ALDI', 'LIDL'\
                'AUCHAN', 'AKTIV MARKT LUKASIEWICZ', 'CITTI', 'SUPERMERCATO', 'KONDITOREI JUNGE'\
                , 'LANDWEGE', 'E-CENTER' ]

dict_essen = {'Restaurant':list_restaurant, 'Einkauf':list_einkauf}
for key, value in dict_essen.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)


#HAUSHALT
list_handy = ['CONGSTAR']
list_baumarkt = ['BAUHAUS', 'HELLWEG']
list_mobility = ['DB VERTRIEB']
list_steuern = ['BEZIRKSREGIERUNG']
list_miete = ['MIETE']
list_bank = ['ABSCHLUSSPOSTEN']
list_hausrat = ['SCHLESWIGER VERSICH']
list_haushalt_sonstiges = ['UEBERSPACE', 'DEUTSCHE POST', 'WARENHAUS WALTROP', 'APOTHEKE']

dict_haushalt = {'Handy':list_handy, 'Baumarkt':list_baumarkt, 'Mobility':list_mobility\
                , 'Steuern':list_steuern, 'Miete':list_miete, 'Bank':list_bank\
                , 'Haushalt Sonstiges':list_haushalt_sonstiges, 'Hausrat':list_hausrat}
for key, value in dict_haushalt.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)
#AUTO
list_tanken = ['SHELL', 'SB TANK', 'AVIA', 'OIL TANK', 'ORLEN', 'JET', 'WESTFALEN TS'\
                , 'Aral']
list_auto_steuern = ['BUNDESKASSE IN KIEL']
list_auto_versicherung = ['HDI']
list_auto_sonstiges = ['SCHLUESSEL-REESE']

dict_auto = {'Tanken':list_tanken, 'Auto Steuern':list_auto_steuern\
            , 'Auto Versicherung':list_auto_versicherung\
            , 'Auto Sonstiges':list_auto_sonstiges}
for key, value in dict_auto.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)

#FIRMA
list_parken = ['Flughafen Hamburg', 'HAMBURG AIRPORT']
list_taxi = ['Payco Taxi', 'PAYCO', 'TAXI FRANKFURT']
list_firma_mobility = ['VBK-VERKEHRSBETRIEBE KARLS']

dict_firma = {'Parken':list_parken, 'Taxi':list_taxi\
            , 'Firma Mobility':list_firma_mobility}
for key, value in dict_firma.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)

#SPORT
list_fitnessstudio = [ 'MCFIT', 'FITX']
list_sportartikel = ['DECATHLON', 'SURF-CENTER']

dict_sport = {'Fitnessstudio':list_fitnessstudio, 'Sportartikel':list_sportartikel}
for key, value in dict_sport.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)

#SONSTIGES
list_sonstiges = ['TABAK', 'TRACKS + TAKE OFF', 'LUCKY BIKE', 'Bernd', 'Reservix']
list_sonstiges_spenden = ['EVG LANDWEGE eG']
dict_sonstiges = {'Sonstiges':list_sonstiges, 'Spenden':list_sonstiges_spenden}
for key, value in dict_sonstiges.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x='Sonstiges')
    row = result.fetchone()
    for subvalue in list_sonstiges:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)

#EINNAHMEN
list_gehalt = ['NTT']
list_einnahmen_sonstiges = ['OMA', 'HONOR 8', 'COMUTO','Frederic Krehl']
list_einnahmen_steuern = ['STEUERVERWALTUNG NRW']

dict_einnahmen = {'Gehalt':list_gehalt, 'Einnahmen Sonstiges':list_einnahmen_sonstiges\
                    , 'Einnahmen Steuern':list_einnahmen_steuern}
for key, value in dict_einnahmen.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)
#KREDITKARTE
list_kreditkarte = [ 'KREDITKARTE' ]

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x='Kreditkarte')
row = result.fetchone()
for subvalue in list_kreditkarte:
    conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)

#BARGELD
list_bargeld = ['AUSZAHLUNG']

conn = haushaltsbuch_db.connect()
result = conn.execute(select_stmt, x='Auszahlung')
row = result.fetchone()
for subvalue in list_bargeld:
    conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)

#SPAREN
list_sparplan = ['ETF-Sparplan', 'Lukas']
list_sparbuch = ['Sparbuch']
list_sonstige_investments = ['Auxmoney', 'Aktien']

dict_sparen = {'Sparplan':list_sparplan, 'Sparbuch':list_sparbuch\
                    , 'Sonstige Investments':list_sonstige_investments}
for key, value in dict_sparen.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)

#ALEX+LUKAS
list_gemeinsame_moebel = ['IKEA', 'Fink, Arne', 'KUECHE 1']
list_sonstige_gemeinsame_ausgaben = ['Frieda Bühl', 'Verk.iersverbond', 'FUENFUNDDREISSIG'\
                                    , 'PEAK PERFORMANCE', 'Schleswiger Versicherungsservice AG']

dict_al = {'Gemeinsame Moebel':list_gemeinsame_moebel\
                    , 'AL Sonstiges':list_sonstige_gemeinsame_ausgaben}
for key, value in dict_al.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)
#URLAUB
list_urlaub_sardinien = ['MORISCA', 'URLAUB']
list_urlaub_ski = ['VIKTORIA BOSS', '8 A HUIT']

dict_urlaub = {'Urlaub Sardinien':list_urlaub_sardinien, 'Urlaub Ski':list_urlaub_ski}
for key, value in dict_urlaub.items():
    conn = haushaltsbuch_db.connect()
    result = conn.execute(select_stmt, x=key)
    row = result.fetchone()
    for subvalue in value:
        conn.execute(ins, haendlerkategorie_id=row[0], auftraggeber=subvalue)

'''
UMSATZART
'''
ins = cl_umsatzart.insert()
conn = haushaltsbuch_db.connect()
umsatzart = ["Auszahlung Geldautomat", "Kartenzahlung", "Kreditkarte", "SEPA-Dauerauftrag an"\
            , "SEPA-Gutschrift von", "SEPA-Lastschrift (ELV) von", "SEPA-Lastschrift von"\
            , "SEPA-Überweisung an"]
for art in umsatzart:
    conn.execute(ins, umsatzart=art)

'''
ORT
'''
ins = cl_ort.insert()
conn = haushaltsbuch_db.connect()
staedte = ['Dortmund', 'Luebeck', 'Sandesneben', 'Kassel', 'Karlsruhe', 'Luxembourg', 'Hamburg', 'Cagliari'\
            , 'Bochum', 'Gothenburg'
            ]
for city in staedte:
    geolocator = geo.Nominatim()
    location = geolocator.geocode(city, timeout=10)
    try:
        conn.execute(ins, stadt=city, lat=location.latitude, lon=location.longitude)
    except:
        print('Error for city:', city)
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])



