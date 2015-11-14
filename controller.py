# -*-coding: utf-8-*-
from flask import Flask, render_template, request, redirect, session
import subprocess, requests, urllib2

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'


@app.route("/login", methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        r = requests.post(
            "https://api.t411.in/auth",
            data={
                "username": request.form['login'],
                "password": request.form['password']
            }
        )
        r = r.json()

        if "error" in r:
            message = r['error']
        else:
            session["token"] = r['token']
            return redirect("/")

    return render_template("login.html", message=message)


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session["token"] = ""
    return redirect("/")


@app.route("/", methods=['POST', 'GET'])
def index():

    # On vérifie si l'utilisateur est connecté sinon
    # on redirige vers la page d'authentification
    if len(session["token"]) == 0:
        return redirect("/login")

    r = requests.get(
        "http://api.t411.in/categories/tree",
        headers={'Authorization': session["token"]}
    )
    categories = r.json()

    list_categories = []
    for categorie in categories['210']['cats']:
        list_categories.append({
            "id": categories['210']['cats'][categorie]["id"],
            "name": categories['210']['cats'][categorie]["name"]
        })

    list_video = []
    if "search" in request.form:
        id_categorie = 0
        if "id_categorie" in request.form:
            id_categorie = request.form["id_categorie"]

        search = request.form['search']
        r = requests.get(
            "http://api.t411.in/torrents/search/%s?offset=10&limit=50" % search.replace(" ", "+"),
            #"http://api.t411.in/torrents/search/%s" % search.replace(" ", "+")+ "?cat="+ id_categorie,
            headers={'Authorization': session['token']}
        )
        response = r.json()
        for entry in response['torrents']:
            list_video.append({"id": entry['id'], "name": entry['name']})

    return render_template(
        "content.html",
        token=session['token'],
        list_video=list_video,
        list_categories=list_categories
    )


@app.route("/download", methods=['POST', 'GET'])
def download():

    # On vérifie si l'utilisateur est connecté sinon
    # on redirige vers la page d'authentification
    if len(session["token"]) == 0:
        return redirect("/login")

    if "id" in request.form:
        id = request.form['id']

        response = urllib2.urlopen(
            "http://api.t411.in/torrents/details/%d"%id,
            headers={'Authorization': session['token']}
        )
        html = response.read()

    return redirect("/")


@app.route("/play", methods=['POST', 'GET'])
def playt():
    id = request.args["id"]
    url = "http://api.t411.in/torrents/download/"+id
    subprocess.check_call(["peerflix '%s' --omx&" % url], shell=True)
    print url
    return ''


@app.route("/stop", methods=['POST', 'GET'])
def stop():
    print "stop"
    try: subprocess.check_call(["pgrep 'youtube-dl|omxplayer.bin|peerflix'|sudo xargs kill"], shell=True)
    except: pass
    return ''

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8001,debug=True)