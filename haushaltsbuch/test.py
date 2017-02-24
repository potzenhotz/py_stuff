import geopy as geo

geolocator = geo.Nominatim()

location = geolocator.geocode('LUEBECK')
print(location.address)
#print(dir(location))
print(dir(location.address))

