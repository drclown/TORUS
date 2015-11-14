# -*-coding: utf-8-*-
import requests

token = "99899083:314:209cf6aa1e7f1113120ca73a60701657"
id_categorie = 633
search = 'avatar'
r = requests.get(
    #"http://api.t411.in/torrents/search/%s" % search.replace(" ", "+"),
    #"http://api.t411.in/torrents/search/%s" % (search.replace(" ", "+")+"?cat="+str(id_categorie)),
    "http://api.t411.in/torrents/search/avatar?cat=1    ",
    headers={'Authorization': token}
)
response = r.json()

list_video = []
for entry in response['torrents']:
    list_video.append({"id": entry['id'], "name": entry['name']})
print(list_video)
