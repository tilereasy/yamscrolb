from yandex_music import Client
from yandex_music.utils.request import Request
import pylast

import time
import os
import sys

SCROBBLE_COOLDOWN = 15
FULLMODELSCOUNT = 2

def get_last_fm_password():
    if os.environ.get("LASTFM_PASSWORD") != None and os.environ.get("LASTFM_PASSWORD") != "":
        return os.environ.get("LASTFM_PASSWORD")
    elif os.environ.get("LASTFM_PASSWORD_HASH") != None and os.environ.get("LASTFM_PASSWORD_HASH") != "":
        return os.environ.get("LASTFM_PASSWORD_HASH")
    else:
        print("Отсутвствует пароль или хэш пароля Last FM!")
        sys.exit()

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

user_data = {"TOKEN_YANDEX":os.environ.get("TOKEN_YANDEX"),
                 "TOKEN_LASTFM":os.environ.get("TOKEN_LASTFM"),
                 "SECRET_LASTFM":os.environ.get("SECRET_LASTFM"),
                 "LASTFM_LOGIN": os.environ.get("LASTFM_LOGIN"),
                 "LASTFM_PASSWORD_HASH":os.environ.get("LASTFM_PASSWORD_HASH"),
                 "LASTFM_PASSWORD":get_last_fm_password(),
                 "COOKIE":os.environ.get("COOKIE")}

REQUIRED_ENV = ["TOKEN_YANDEX", "TOKEN_LASTFM", "SECRET_LASTFM", "LASTFM_LOGIN"]
missing = [var for var in user_data if not user_data[var]]
if missing:
    print(f"Отсутствует {missing} в переменных окружения!")

try:
    client = Client(user_data["TOKEN_YANDEX"])
    client.init()
    print("Авторизован на Яндекс Музыке!")
except:
    print("Ошибка при авторизации на Яндекс Музыке!")
    sys.exit()


try:
    session = pylast.LastFMNetwork(
    api_key=user_data["TOKEN_LASTFM"],
    api_secret=user_data["SECRET_LASTFM"],
    username=user_data["LASTFM_LOGIN"],
    password_hash=user_data["LASTFM_PASSWORD"])
    print("Авторизован на Last FM!\n")
except:
    print("Ошибка при авторизации на Last FM!")
    sys.exit()

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

