import time
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from riotwatcher import LolWatcher, ApiError

app = Flask(__name__)
api_key = 'RGAPI-a2dafc3e-f256-41bd-a9f9-aab49177d2c7'
watcher = LolWatcher(api_key)
MY_REGION = 'euw1'
SUMMONER_NAME = "P1ncel"
versions = watcher.data_dragon.versions_for_region(MY_REGION)
summoner = watcher.summoner.by_name(MY_REGION, SUMMONER_NAME)
champions_version = versions['n']['champion']
CHAMPION_LIST = watcher.data_dragon.champions(champions_version)
in_match = False


@app.route('/', methods=['GET'])
def home():
    msg=""
    try:
        watcher.spectator.by_summoner(MY_REGION, summoner['id'])
    except ApiError as err:
        if err.response.status_code == 404:
            msg = " no está en partida"
    else:
        msg = " está en partida"
    return render_template("index.html", msg=msg)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)