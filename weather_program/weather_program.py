#!/usr/bin/env python3
#Weather program using OpenWeatherMap

import weather_script as ws
import useful_stuff as us
import os
import sys

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
              ,'LukasWork': 'lukas.muessle@nttdata.com' 
              ,'Florian': 'florian@mail-arends.de' 
              ,'Frederic': 'frederic.krehl@nttdata.com' 
              }

#lukas_cities = ['Koeln', 'Duesseldorf','Dortmund']
lukas_cities = ['Koeln']
lukas_work_cities = ['Duesseldorf']
alex_cities = ['Luebeck']
florian_cities = ['Duesseldorf']
frederic_cities = ['Muenchen']

user_cities = {'Lukas': lukas_cities
            ,'Alex': alex_cities
            ,'LukasWork': lukas_work_cities
            ,'Florian': florian_cities
            ,'Frederic': frederic_cities
            }

#users = ['Lukas', 'Alex', 'LukasWork', 'Florian', 'Frederic']
users = ['Lukas', 'LukasWork', 'Alex']
#users = ['Lukas', 'LukasWork']
#users = ['Lukas']
#users = ['Florian']

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
    email_on=1

    if email_on == 1:
      text_format = 'html'
    else:
      text_format = 'plain'
    subject = 'Wetterbericht fuer ' + str(user) + ' [PROTOTYP]'

    #body of email
    try:
      body_msg = 'Diese Staedte hast du abonniert:'
      for cities_var in user_cities[user]:
        body_msg += str(ws.current_weather(city_dict[cities_var]))
        body_msg += '\n'
    except OSError as err:
      print("OS error: {0}".format(err))
    except ValueError:
      print("%%%Value Error.%%%")
    except KeyError:
      print("%%%City name error.%%%", sys.exc_info())

    except:
      print("Unexpected error:", sys.exc_info()[0])
      raise  

    
    #converts \n into html code
    if text_format == 'html':
      body_msg = body_msg.replace("\n", "<br />")
      bold_open='<b>'
      bold_close='</b>'
      body_msg = body_msg.replace(us.color.BOLD, bold_open)
      body_msg = body_msg.replace(us.color.END, bold_close)


    #send actual mail in html oder plain text 
    if email_on == 1:
      us.send_mail(to_addrs, subject, body_msg, pwd_mail, text_format)
    else:
      print(body_msg)
  

