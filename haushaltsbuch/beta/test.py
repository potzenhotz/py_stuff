import geopy as geo

geolocator = geo.Nominatim()

location = geolocator.geocode('Luebeck')
#location = geolocator.geocode('Cagliari')
print(location.address)
#print(dir(location))
#print(dir(location.address))
print((location.latitude, location.longitude))
print(location.raw)
