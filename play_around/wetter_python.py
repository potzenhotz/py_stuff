

#python script for rss feed read of weather data

import pyowm

owm = pyowm.OWM('770bab8b8abf5696883cf53b96333e9f')

# You have a pro subscription? Use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

# Will it be sunny tomorrow at this time in Milan (Italy) ?
forecast = owm.daily_forecast("Hamburg,ger")
tomorrow = pyowm.timeutils.tomorrow()
d=forecast.will_be_sunny_at(tomorrow)  # Always True in Italy, right? ;-)
print(d)
#print('Forecast on %s is : %s' % (tomorrow, forecast.will_be_sunne_at(tomorrow)))

# Search for current weather in London (UK)
observation = owm.weather_at_place('Hamburg,ger')
w = observation.get_weather()
print(w)               

print(w.get_wind()) 
print(w.get_humidity()) 
print(w.get_temperature()) 

for parts in dir(w):
  print(parts)
print('##################################')
for parts in dir(forecast):
  print(parts)
print('##################################')
for parts in dir(owm):
  print(parts)
