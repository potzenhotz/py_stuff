#!/usr/bin/env python3
#Weather program using OpenWeatherMap


import weather_script as ws
import useful_stuff as us
import os

#-----------------------------------------------------------------------
#Dictionaries for Cities and Users(Email)
#-----------------------------------------------------------------------


city_dict = {'Dortmund': 'Dortmund' + ', ger'
            ,'Hamburg': 'Hamburg' + ', ger'
            ,'Luebeck': 'Luebeck' + ', ger'
            ,'Koeln': 'Koeln' + ', ger'
            ,'Duesseldorf': 'Duesseldorf' + ', ger'
            ,'Muenchen': 'Muenchen' + ', ger'
            }

email_dict = {'Lukas': 'lukasmuessle@gmail.com'
              ,'Alex': 'a.craemer@gmail.com' 
              }

#lukas_cities = ['Koeln', 'Duesseldorf','Dortmund']
lukas_cities = ['Koeln', 'Duesseldorf']
alex_cities = ['Luebeck']

user_cities = {'Lukas': lukas_cities
            ,'Alex': alex_cities
            }

users = ['Lukas']

for user in users:
  #-----------------------------------------------------------------------
  #Testing area
  #-----------------------------------------------------------------------
  test_flag = 0
  
  if test_flag == 1:
    #for keys in city_dict:
    #  ws.current_weather(city_dict[keys])
    print(ws.current_weather(city_dict['Koeln']))
  
  else:  
    #-----------------------------------------------------------------------
    #Email configuration
    #-----------------------------------------------------------------------
    pwd_file_name = 'python_mailing_bot.txt'
    pwd_file_loc = os.environ['HOME'] + '/Documents/'
   
    #reads first line of the file 
    pwd_mail = us.read_certain_line(pwd_file_name,pwd_file_loc,0)
    
    email_dict_keys_list = list(email_dict.keys())
    to_addrs  = email_dict[user]
  
    #setup the email subject
    subject = 'Wetterbericht fuer ' + str(user) + ' [PROTOTYP]'

    #body of email
    body_msg = 'Diese Staedte hast du aboniert:'
    for cities_var in user_cities[user]:
      body_msg += str(ws.current_weather(city_dict[cities_var]))
      body_msg += '\n'
  
    #print(body_msg)
    #send actual mail 
    us.send_mail(to_addrs, subject, body_msg, pwd_mail)
  

