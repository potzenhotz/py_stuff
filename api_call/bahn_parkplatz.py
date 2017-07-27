#/bin/python3

import requests

req_string= 'http://opendata.dbbahnpark.info/api/beta/occupancy'
response = requests.get(req_string)


print('Printing status code: \n{0}'.format(response.status_code))
print('Printing headers: \n{0}'.format(response.status_code))
print('Printing status code: \n{0}'.format(response.text[0:200]))
#print('Printing status code {0}'.format(response.json()))


