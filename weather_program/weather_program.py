#Weather program using OpenWeatherMap

import weather_script as ws


city_dict = {'Dortmund' : 'Dortmund' + ', ger'
            ,'Hamburg' : 'Hamburg' + ', ger'
            ,'Luebeck' : 'Luebeck' + ', ger'
            }

#for keys in city_dict:
#  ws.current_weather(city_dict[keys])

ws.current_weather(city_dict['Dortmund'])
