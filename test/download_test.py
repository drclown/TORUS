# -*-coding: utf-8-*-
import requests
import os
import shutil

token = '99899083:314:209cf6aa1e7f1113120ca73a60701657'
url = "http://api.t411.in/torrents/downloads/136212"
response = requests.get(
    url,
    headers={'Authorization': token}
)
print(response)
dump = response.raw

location = os.path.abspath("D:\\caca.torus")
with open("D:\\caca.torus", 'wb') as location:
    shutil.copyfileobj(dump, location)

print(dump)