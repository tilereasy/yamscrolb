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

def format_track(title, artists):
    return f"{', '.join(artists)} — {title}"

def get_current_track(request):
    try:
        response = request.get(f"https://api.music.yandex.ru/music-history?fullModelsCount={FULLMODELSCOUNT}")
        title = get_title(response)
        artists = get_artists(response)
        return title, artists, format_track(title, artists)
    except Exception as error:
        print(f"Не удалось получить историю Яндекс Музыки: {error}")
        print("Проверьте COOKIE: для endpoint music-history требуется cookie авторизованного браузера.")
        return None

def scrobble(session, title, artists):
    session.scrobble(artists[0], title, timestamp=get_timestamp())
    print(format_track(title, artists))


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

REQUIRED_ENV = ["TOKEN_YANDEX", "TOKEN_LASTFM", "SECRET_LASTFM", "LASTFM_LOGIN", "COOKIE"]
missing = [var for var in REQUIRED_ENV if not user_data[var]]
if missing:
    print(f"Отсутствует {missing} в переменных окружения!")
    sys.exit()

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

request = Request(client, {"Cookie": user_data["COOKIE"]})
last_track = None

while True:
    track = get_current_track(request)
    if track:
        title, artists, current_track = track
        if last_track is None:
            last_track = current_track
        elif current_track != last_track:
            last_track = current_track
            try:
                scrobble(session, title, artists)
            except Exception as error:
                print(f"Возникла проблема при скробблинге: {error}")
    time.sleep(SCROBBLE_COOLDOWN)

