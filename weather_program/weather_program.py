#Weather program using OpenWeatherMap

import weather_script as ws
import useful_stuff as us

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


pwd_file_name = 'python_mailing_bot.txt'
pwd_file_loc = '/Users/Potzenhotz/Documents/'


pwd_mail = us.read_certain_line(pwd_file_name,pwd_file_loc,0)
#for keys in city_dict:
#  ws.current_weather(city_dict[keys])

print(ws.current_weather(city_dict['Koeln']))


to_addrs  = email_dict['Lukas']
email_dict_keys_list = list(email_dict.keys())
subject = 'Wetterbericht fuer ' + str(email_dict_keys_list[0]) + ' [PROTOTYP]'
body_msg = str(ws.current_weather(city_dict['Dortmund']))

#us.send_mail(to_addrs, subject, body_msg, pwd_mail)

