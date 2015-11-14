# -*-coding: utf-8-*-
import requests

r = requests.Session().post('https://api.t411.in/auth',
    data={
        "username": "frouttine",
        "password": "motdepasse"
    }
);
r = r.json()
if "error" in r:
    print(r['error'])
#print(r['error'])
#token = r['token']

#print(token)
