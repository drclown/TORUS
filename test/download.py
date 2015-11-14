# -*-coding: utf-8-*-
from flask import Flask, render_template, request, redirect, session, sessions
import requests
import urllib2

id = 5300396
token = '99899083:313:fe2789a4e6885d62544a267963ea24d4'
r = requests.get(
    "http://api.t411.in/torrents/download/%s"%id,
    headers={'Authorization': token}
)
dump = r.raw
print(type(dump))