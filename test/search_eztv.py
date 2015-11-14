# -*-coding: utf-8-*-
import requests
import re

search = "american horror story"

list_video = []

res = requests.post("http://eztv.it/showlist/")
res = re.compile("/shows/([^/]+)/([^/]+)").findall(res.text)
search = search.split(" ")
for (_id, title) in res:
    valid = True
    for s in search:
        if s not in title:
            valid = False
            break
    if valid:
        list_video.append((_id, title))

#print(list_video)

res = requests.post("http://eztv.it/shows/%s/" % search)
print(res.text)
episodes = re.compile("/ep/[^/]+/([^/]+)").findall(res.text)
magnets = re.compile('a href="(magnet[^"]+)"').findall(res.text)
#print(magnets)
