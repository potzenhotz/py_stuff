#Python script for rss feed read of weather data

import pyowm
from pyowm import timeutils
from datetime import datetime
import time

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
  today_06 = str(time.strftime("%Y-%m-%d")) + ' 06:00:00+00'
  today_09 = str(time.strftime("%Y-%m-%d")) + ' 09:00:00+00'
  today_12 = str(time.strftime("%Y-%m-%d")) + ' 12:00:00+00'
  today_15 = str(time.strftime("%Y-%m-%d")) + ' 15:00:00+00'
  today_18 = str(time.strftime("%Y-%m-%d")) + ' 18:00:00+00'
  tomorrow_06=str(timeutils.tomorrow(6,00)) + '+00'
  tomorrow_09=str(timeutils.tomorrow(9,00)) + '+00'
  tomorrow_12=str(timeutils.tomorrow(12,00)) + '+00'
  tomorrow_15=str(timeutils.tomorrow(15,00)) + '+00'
  tomorrow_18=str(timeutils.tomorrow(18,00)) + '+00'

  fc_times_today = [today_06
                    ,today_09
                    ,today_12
                    ,today_15
                    ,today_18]
  fc_times_tomorrow = [tomorrow_06
                    ,tomorrow_09
                    ,tomorrow_12
                    ,tomorrow_15
                    ,tomorrow_18]


  output ='\n' + '###%s### %s(%s, %s)' % (time_of_obs,city,lat,lon)
  fc_object_3h = owm.three_hours_forecast(input_city)  
  fc_object_daily = owm.daily_forecast(input_city, limit=4)  

  observat = obs.get_weather()
  f_3h = fc_object_3h.get_forecast()
  f_daily = fc_object_daily.get_forecast()

  weather_dict = {'forecast3':f_3h,'forecast_daily': f_daily,'observation': observat}
  #for weather in weather_list: 
  for key in sorted(weather_dict):
    weather = weather_dict[key]
    if key == 'observation':
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

    today_fc_3h = 'Forecast for today:'
    tomorrow_fc_3h = 'Forecast for tomorrow:'
    seven_days_fc = 'Forecast for today and the next 3 days:'
    if key == 'forecast3':
      for weather_part in weather:
        for times in fc_times_today:
          #if weather.get_reference_time('iso') == times: 
          if weather_part.get_reference_time('iso') == times: 
            time_string = str(weather_part.get_reference_time('iso'))
            time_string = time_string[:-6]
            today_fc_3h += '\n' + time_string + ' '+ str(weather_part.get_status())
        for times in fc_times_tomorrow:
          if weather_part.get_reference_time('iso') == times:
            time_string = str(weather_part.get_reference_time('iso'))
            time_string = time_string[:-6]
            tomorrow_fc_3h += '\n' + time_string + ' ' + str(weather_part.get_status())
            
    if key == 'forecast_daily':
      for weather_part in weather:
        time_string = str(weather_part.get_reference_time('iso'))
        time_string = time_string[:-6]
        seven_days_fc += '\n' + '[STATUS] ' + time_string + '\nForecast: '+ str(weather_part.get_status())
          
        fc_temp_daily = weather_part.get_temperature(unit='celsius')
        fc_temp_daily_morn = str(fc_temp_daily['morn']) + u'\N{DEGREE SIGN}' + 'C'
        fc_temp_daily_day = str(fc_temp_daily['day']) + u'\N{DEGREE SIGN}' + 'C'
        fc_temp_daily_eve = str(fc_temp_daily['eve']) + u'\N{DEGREE SIGN}' + 'C'
        fc_temp_daily_night = str(fc_temp_daily['night']) + u'\N{DEGREE SIGN}' + 'C'
        fc_temp_daily_max = str(fc_temp_daily['max']) + u'\N{DEGREE SIGN}' + 'C'
        fc_temp_daily_min = str(fc_temp_daily['min']) + u'\N{DEGREE SIGN}' + 'C'
        seven_days_fc += '\n' + '[TEMP] \nMorning: %s \nDay: %s \nEvening: %s \nNight: %s' \
                        % (fc_temp_daily_morn, fc_temp_daily_day, fc_temp_daily_eve, fc_temp_daily_night)

        fc_wind_daily = weather_part.get_wind()
        fc_wind_speed_daily = fc_wind_daily['speed']
        seven_days_fc += '\n' + '[Wind] \n' + 'Average: ' + str(fc_wind_speed_daily) + ' m/s'

        fc_rain_daily_raw = weather_part.get_rain()
        fc_rain_daily = fc_rain_daily_raw['all']
        seven_days_fc += '\n' + '[Precipitation] \n' + 'Rain: ' + str(fc_rain_daily) + ' mm'

        seven_days_fc += '\n'+'-----------------------------------------------------------------'

    #test=fc_object_daily.when_starts('iso')

    #-----------------------------------------------------------------------
    #Print section for testing
    #In future maybee outside
    #-----------------------------------------------------------------------
    if key == 'forecast3':
      output += '\n'+'#################################################################'
      output += '\n' + today_fc_3h
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n' + tomorrow_fc_3h
    if key == 'forecast_daily':
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n' + seven_days_fc
      output += '\n'+'#################################################################'
    if key == 'observation':
      output +='\n' + 'Weather observations %s %s(%s, %s):' % (time_of_obs,city,lat,lon)
      output += '\n'+'-----------------------------------------------------------------'
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
 #output += '\n' + str(test1)
  #output += '\n' + str(test2)
  #output += '\n' + str(test3)
  #output += '\n' + str(test4)
  return output
