#!/bin/python

from InstagramAPI import InstagramAPI
import os

"""
Functions
"""
def read_certain_line(file_name,file_loc,linenumber):
  pwd_file = file_loc + file_name
  open_file = open(pwd_file)
  pwd_read = open_file.readlines()
  #pwd_mail = "".join(pwd_read.split())
  open_file.close()
  return pwd_read[linenumber]


"""
Get credentials for Instagram API
"""
insta_credentials_file = 'instagram.txt'
insta_credentials_folder = os.environ['HOME'] + '/Documents/'

#reads first line of the file 
insta_usr = read_certain_line(insta_credentials_file,insta_credentials_folder,0)
insta_pwd = read_certain_line(insta_credentials_file,insta_credentials_folder,1)

#strip '\n' from string
insta_usr = insta_usr.rstrip()
insta_pwd = insta_pwd.rstrip()

#print(insta_usr)
#print(repr(insta_pwd))

"""
Start Instagram API
"""

#API = InstagramAPI(insta_usr,insta_pwd)
#API.login()


following   = []
next_max_id = True
while next_max_id:
    print(next_max_id)
 
