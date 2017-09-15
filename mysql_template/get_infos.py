#/bin/env python3

import sqlalchemy as sql
import sys




def read_certain_line(file_name,file_loc,linenumber):
  pwd_file = file_loc + file_name
  open_file = open(pwd_file)
  pwd_read = open_file.readlines()
  open_file.close()
  return pwd_read[linenumber]


raw_mysql_pwd = read_certain_line('.my.cnf', '/home/u300202/', 29)
mysql_pwd = raw_mysql_pwd.split()[0].split('=')[1]

#sys.exit()
engine = sql.create_engine('mysql+pymysql://u300202:{0}@localhost/u300202'.format(mysql_pwd))

md = sql.MetaData()

md.reflect(engine)

for table in md.tables.values():
    print(table.name)
    for column in table.c:
        print(column.name)
