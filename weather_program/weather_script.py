

#python script for rss feed read of weather data

import pyowm
from datetime import datetime
#-----------------------------------------------------------------------
#Useful functions
#-----------------------------------------------------------------------
def change_time_format(input):
  output =  datetime.fromtimestamp(input).strftime('%d-%m-%Y %H:%M')
  return output

def pp(input_dict):
  for keys in sorted(input_dict):
    if str(input_dict[keys]) != '{}':
      print(keys + ': ' + str(input_dict[keys]))


#-----------------------------------------------------------------------
#Use my owm key
#-----------------------------------------------------------------------
stadt = 'Dortmund'
stadt_raw = 'Dortmund' + ', ger'


#-----------------------------------------------------------------------
#Use my owm key
#-----------------------------------------------------------------------
owm = pyowm.OWM('770bab8b8abf5696883cf53b96333e9f')

#-----------------------------------------------------------------------
#Setup the observation(obs) for a certain location
#-----------------------------------------------------------------------
obs = owm.weather_at_place(stadt)

time_of_obs_unix = obs.get_reception_time()
time_of_obs =  change_time_format(time_of_obs_unix)

location_raw = obs.get_location()
location_name = location_raw.get_name()
location_id = location_raw.get_ID()
lat = location_raw.get_lat()
lon = location_raw.get_lon()


#-----------------------------------------------------------------------
#Get the weather data of the location object
#-----------------------------------------------------------------------
weather = obs.get_weather()

wind = weather.get_wind()
wind_speed = wind['speed']
wind_deg = wind['deg']
temp = weather.get_temperature(unit='celsius')
temp_max = temp['temp_max']
temp_min = temp['temp_min']
temperature = temp['temp']
pressure = weather.get_pressure()
press_local = pressure['press']
press_sea = pressure['sea_level']
sunrise_unix = weather.get_sunrise_time()
sunrise = change_time_format(sunrise_unix)
sunset_unix = weather.get_sunset_time()
sunset = change_time_format(sunset_unix)

weather_dict = {'Cloud cover': weather.get_clouds()
                ,'Humidity' : str(weather.get_humidity()) + '%'
                ,'Sky' : weather.get_detailed_status()
                ,'Rain volume last 3h' : weather.get_rain()
                ,'Snow volume last 3h' : weather.get_snow()
                ,'Wind speed' : str(wind_speed) + ' m/s'
                ,'Wind deg' : str(wind_deg) + u'\N{DEGREE SIGN}'
                ,'Temperature' : str(temperature) + u' \N{DEGREE SIGN}' + 'C'
                ,'Temp_max' : str(temp_max) + u' \N{DEGREE SIGN}' + 'C'
                ,'Temp_min' : str(temp_min) + u' \N{DEGREE SIGN}' + 'C'
                ,'Pressure' : str(press_local) + ' hPa'
                ,'Pressure at sea level' : str(press_sea) + ' hPa'
                ,'Sunrise' : sunrise
                ,'Sunset' : sunset
                }

wind_dict = {'Wind speed' : str(wind_speed) + ' m/s'
             ,'Wind deg' : str(wind_deg) + u'\N{DEGREE SIGN}'
            }

sky_condition = {'Cloud cover': weather.get_clouds()
                 ,'Sky' : weather.get_detailed_status()
                }

precipitation_dict = {'Humidity' : str(weather.get_humidity()) + '%'
                     ,'Rain volume last 3h' : weather.get_rain()
                     ,'Snow volume last 3h' : weather.get_snow()
                    }
temp_dict = {'Temperature' : str(temperature) + u' \N{DEGREE SIGN}' + 'C'
            ,'Temp_max' : str(temp_max) + u' \N{DEGREE SIGN}' + 'C'
            ,'Temp_min' : str(temp_min) + u' \N{DEGREE SIGN}' + 'C'
            }

sun_dict = {'Sunrise' : sunrise
            ,'Sunset' : sunset
            }

pressure_dict = {'Pressure' : str(press_local) + ' hPa'
                  ,'Pressure at sea level' : str(press_sea) + ' hPa'
                }




#-----------------------------------------------------------------------
#print section
#-----------------------------------------------------------------------
print('Wetter fuer die Stadt: %s' % (stadt))
print('-----------------------------------------------------------------')
pp(sun_dict)
print('-----------------------------------------------------------------')
pp(temp_dict)
print('-----------------------------------------------------------------')
pp(pressure_dict)
print('-----------------------------------------------------------------')
pp(precipitation_dict)
print('-----------------------------------------------------------------')
