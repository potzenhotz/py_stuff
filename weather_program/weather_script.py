#Python script for rss feed read of weather data

import pyowm
from pyowm import timeutils
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

def pp_str(input_dict):
  output = ''
  i = 0
  for keys in sorted(input_dict):
    if str(input_dict[keys]) != '{}':
      if i == 0:
        output +=  str(keys + ': ' + str(input_dict[keys]))
      else:
        output += '\n' + str(keys + ': ' + str(input_dict[keys]))
    i += 1
  return output


#-----------------------------------------------------------------------
#Weather function
#-----------------------------------------------------------------------

def current_weather(input_city):
  
  #-----------------------------------------------------------------------
  #Extract City name
  #-----------------------------------------------------------------------
  city = input_city.split(',', 1)[0]  #input needs to modify with split

  #-----------------------------------------------------------------------
  #Use open weather map key
  #-----------------------------------------------------------------------
  owm = pyowm.OWM('770bab8b8abf5696883cf53b96333e9f')
  
  #-----------------------------------------------------------------------
  #Setup the observation(obs) for a certain location
  #-----------------------------------------------------------------------
  obs = owm.weather_at_place(input_city)
  
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
  


  #One full dict for all weather data
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

  #Different logical specified weather dicts 
  wind_dict = {'Wind speed' : str(wind_speed) + ' m/s'
               ,'Wind direction' : str(wind_deg) + u'\N{DEGREE SIGN}'
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
  #FORECAST
  #-----------------------------------------------------------------------

  fc_object_3h = owm.three_hours_forecast(input_city)  
  fc_object_daily = owm.daily_forecast(input_city, limit=6)  

  f_3h = fc_object_3h.get_forecast()
  f_daily = fc_object_daily.get_forecast()

  time_yesterday = timeutils.yesterday(12, 00) 
  time_tomorrow=timeutils.tomorrow(15,00)
  #test = time_tomorrow
  test1 = fc_object_3h.get_weather_at(timeutils.tomorrow(15,00))
  test = test1.get_clouds()
  time = test1.get_reference_time('iso')

  #test=fc_object_daily.when_starts('iso')

  #-----------------------------------------------------------------------
  #Print section for testing
  #In future maybee outside
  #-----------------------------------------------------------------------
  output =('Wetter fuer die Stadt: %s (%s, %s)' % (city,lat,lon))
  output += '\n'+' -----------------------------------------------------------------'
  output += '\n'+pp_str(sun_dict)
  output += '\n'+'-----------------------------------------------------------------'
  output += '\n'+pp_str(temp_dict)
  output += '\n'+'-----------------------------------------------------------------'
  output += '\n'+pp_str(pressure_dict)
  output += '\n'+'-----------------------------------------------------------------'
  output += '\n'+pp_str(wind_dict)
  output += '\n'+'-----------------------------------------------------------------'
  output += '\n'+pp_str(precipitation_dict)
  output += '\n'+'-----------------------------------------------------------------'
  output += '\n'+pp_str(sky_condition)
  output += '\n'+'-----------------------------------------------------------------'
  output += '\n'+'#################################################################'
  output += str(test)
  output += str(time)
  return output
