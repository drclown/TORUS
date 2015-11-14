# -*-coding: utf-8-*-
import requests

token = "99899083:314:209cf6aa1e7f1113120ca73a60701657"

search = 'avatar'
headers = {'Authorization':'token %s' % token}
r = requests.get(
    "http://api.t411.in/torrents/details/4964318",
    headers={'Authorization': token}
)
response = r.json()

print(response)