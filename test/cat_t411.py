# -*-coding: utf-8-*-
# -*-coding: utf-8-*-
import requests

token = "99899083:314:209cf6aa1e7f1113120ca73a60701657"

headers = {'Authorization':'token %s' % token}
r = requests.get(
    "http://api.t411.in/categories/tree",
    headers={'Authorization': token}
)
categories = r.json()

#print(cats_multimedia)
#print(categories['210']['cats']['631']['name'])

#print(len(categories['210']['cats']))

list_categories = []
for categorie in categories['210']['cats']:
    list_categories.append({
        "id": categories['210']['cats'][categorie]["id"],
        "name": categories['210']['cats'][categorie]["name"]
    })

print(list_categories)