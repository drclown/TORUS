from flask import Flask, render_template, request
import subprocess, re, ast, requests

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    list_video = []
    type_result = None
    if "search" in request.form:
        search = request.form["search"]
        provider = request.form["provider"]
        if provider == "movie":
            type_result = "movies"
            res = ast.literal_eval(requests.post("https://yts.re/api/list.json?keywords=%s" % (search.replace(" ", "+"))).text)
            for entry in res["MovieList"]:
                if entry["State"] == "OK":
                    title = entry["MovieTitleClean"]
                    cover = entry["CoverImage"]
                    torrent = entry["TorrentUrl"]
                    magnet = entry["TorrentMagnetUrl"]
                    peers = entry["TorrentPeers"]
                    quality = entry["Quality"]
                    list_video.append((title, cover, torrent, magnet, peers, quality))
        elif provider == "shows":
            type_result = "shows"
            res = requests.post("http://eztv.it/showlist/")
            res = re.compile("/shows/([^/]+)/([^/]+)").findall(res.text)
            search=search.split(" ")
            for (_id, title) in res:
                valid = True
                for s in search:
                    if s not in title:
                        valid = False
                        break
                if valid:
                    list_video.append((_id, title))
        elif provider == "shows_":
            type_result = "show"
            res = requests.post("http://eztv.it/shows/%s/" % search)
            episodes = re.compile("/ep/[^/]+/([^/]+)").findall(res.text)
            magnets = re.compile('a href="(magnet[^"]+)"').findall(res.text)
            for i, episode in enumerate(episodes):
                list_video.append((episode, magnets[i]))
    return render_template("content.html", list_video=list_video, type_result=type_result)


@app.route("/play", methods=['POST', 'GET'])
def playt():
    url = request.args["url"]
    subprocess.check_call(["peerflix '%s' --vlc&" % url], shell=True)
    print url
    return ''


@app.route("/stop", methods=['POST', 'GET'])
def stop():
    print "stop"
    try: subprocess.check_call(["pgrep 'youtube-dl|omxplayer.bin|peerflix'|sudo xargs kill"], shell=True)
    except: pass
    return ''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
