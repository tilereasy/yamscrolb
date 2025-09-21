from yandex_music import Client
from yandex_music.utils.request import Request
from pathlib import Path
import pylast

import time
import os
import sys

SCROBBLE_COOLDOWN = 15
FULLMODELSCOUNT = 2

def get_timestamp():
    return str(int(time.time()))

def get_title(response, number=0):
    return response["history_tabs"][0]["items"][0]["tracks"][number]["data"]["full_model"]["title"]

def get_artists(response, number=0):
    artists = []
    for i in response["history_tabs"][0]["items"][0]["tracks"][number]["data"]["full_model"]["artists"]:
        artists.append(i["name"])
    return artists

def scrobble(session, title, artists):
    session.scrobble(artists[0], title, timestamp=get_timestamp())
    print(f"{", ".join(artists)} — {title}")

os.system("clear" if os.name=="posix" else "cls")
print(r"                                                                          $$\ $$\       ")  
print(r"                                                                          $$ |$$ |      ")   
print(r"$$\   $$\  $$$$$$\  $$$$$$\$$$$\   $$$$$$$\  $$$$$$$\  $$$$$$\   $$$$$$\  $$ |$$$$$$$\  ")
print(r"$$ |  $$ | \____$$\ $$  _$$  _$$\ $$  _____|$$  _____|$$  __$$\ $$  __$$\ $$ |$$  __$$\ ")
print(r"$$ |  $$ | $$$$$$$ |$$ / $$ / $$ |\$$$$$$\  $$ /      $$ |  \__|$$ /  $$ |$$ |$$ |  $$ |")
print(r"$$ |  $$ |$$  __$$ |$$ | $$ | $$ | \____$$\ $$ |      $$ |      $$ |  $$ |$$ |$$ |  $$ |")
print(r"\$$$$$$$ |\$$$$$$$ |$$ | $$ | $$ |$$$$$$$  |\$$$$$$$\ $$ |      \$$$$$$  |$$ |$$$$$$$  |")
print(r" \____$$ | \_______|\__| \__| \__|\_______/  \_______|\__|       \______/ \__|\_______/ ")
print(r"$$\   $$ |                                                                              ")                                                                        
print(r"\$$$$$$  |                                                                              ")                                                                        
print(r" \______/                                                                               ") 
print("")
print("")

try:
    user_data = {"TOKEN_YANDEX":os.environ.get("TOKEN_YANDEX"),
                 "TOKEN_LASTFM":os.environ.get("TOKEN_LASTFM"),
                 "SECRET_LASTFM":os.environ.get("SECRET_LASTFM"),
                 "LASTFM_LOGIN": os.environ.get("LASTFM_LOGIN"),
                 "LASTFM_PASSWORD_HASH":os.environ.get("LASTFM_PASSWORD_HASH"),
                 "LASTFM_PASSWORD":os.environ.get("LASTFM_PASSWORD"),
                 "COOKIE":os.environ.get("COOKIE")}
except:
    print("Ошибка при считывании данных из переменных окружения!")
    sys.exit()

if user_data["LASTFM_PASSWORD"] == None:
    user_data["LASTFM_PASSWORD"] = user_data["LASTFM_PASSWORD_HASH"]

try:
    client = Client(user_data["TOKEN_YANDEX"])
    client.init()
    print("Авторизован на Яндекс Музыке!")
except:
    print("Ошибка при авторизации на Яндекс Музыке!")


try:
    session = pylast.LastFMNetwork(
    api_key=user_data["TOKEN_LASTFM"],
    api_secret=user_data["SECRET_LASTFM"],
    username=user_data["LASTFM_LOGIN"],
    password_hash=user_data["LASTFM_PASSWORD"])
    print("Авторизован на Last FM!\n")
except:
    print("Ошибка при авторизации на Last FM!")

request = Request(client, {"Cookie":user_data["COOKIE"]})
response = request.get(f"https://api.music.yandex.ru/music-history?fullModelsCount={FULLMODELSCOUNT}")
last_track = f"{", ".join(get_artists(response))} — {get_title(response)}"

while True:
    try:
        response = request.get(f"https://api.music.yandex.ru/music-history?fullModelsCount={FULLMODELSCOUNT}")
        current_track = f"{", ".join(get_artists(response))} — {get_title(response)}"
        if current_track != last_track:
            last_track = current_track
            scrobble(session, get_title(response), get_artists(response))
    except:
        print("Возникла проблема при скробблинге!")
    time.sleep(SCROBBLE_COOLDOWN)

