import urllib.request
import json
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key='AIzaSyCxXp01-Oe7JfuR6J5lk9wPgqsNo3B6t8g'
origin=input('where are you?:').replace(' ','+')

destination=input('where do you want to go?:').replace(' ','+')

nav_request='origin={}&destination={}&key={}'.format(origin,destination,api_key)

request=endpoint+nav_request
response=urllib.request.urlopen(request).read()
directions=json.loads(response)
print(directions)