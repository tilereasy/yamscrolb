from yandex_music import Client
from yandex_music.utils.request import Request
from pathlib import Path
import pylast
import dotenv

import time
import os
import sys

SCROBBLE_COOLDOWN = 15
FULLMODELSCOUNT = 2
DOTENV_FILE = Path(".env")
DOTENV_TEMPLATE = """# Ваш токен Яндекс Музыки
TOKEN_YANDEX=
# Токен приложения Last FM
TOKEN_LASTFM=
# Секретный токен приложения Last FM
SECRET_LASTFM=
# Ваш логин(юзернейм) Last FM
LASTFM_LOGIN=
# Ваш пароль от Last FM
# Можно ввести либо в форме md5-хэша в соответствующее поле
# ЛИБО сам пароль в нехэшированном виде в LASTFM_PASSWORD
# ПРИЧЕМ достаточно заполнить лишь одно из этих полей
# !! Рекомендую ввести именно хэш !!
LASTFM_PASSWORD_HASH=
LASTFM_PASSWORD=
# Значение cookie из браузера где
# вы авторизованы в Яндекс Музыке
# Заполнять необязательно, но
# при отсутствии будут наблюдаться проблемы со скробблингом
COOKIE=
"""

def ensure_dotenv():
    if not DOTENV_FILE.exists():
        print("Файл .env не найден, создаю шаблон...")
        DOTENV_FILE.write_text(DOTENV_TEMPLATE)
        DOTENV_FILE.chmod(0o600)
        print(f"Создан {DOTENV_FILE}, заполните его данными.")
        sys.exit()

def trouble_dotenv(data):
    match data:
        case "TOKEN_YANDEX":
            print("Токен Яндекс Музыки не обнаружен!\n " \
            "Он должен находиться в TOKEN_YANDEX в .env\n")
        case "TOKEN_LASTFM":
            print("Токен приложения Last FM не обнаружен!\n " \
            "Он должен находиться в TOKEN_LASTFM в .env\n")
        case "SECRET_LASTFM":
            print("Secret приложения Last FM не обнаружен!\n " \
            "Он должен находиться в SECRET_LASTFM в .env\n")
        case "LASTFM_LOGIN":
            print("Логин пользователя Last FM не обнаружен!\n " \
            "Он должен находиться в LASTFM_LOGIN в .env\n")
        case "PASSWORD":
            print("Не обнаружено пароля пользователя Last FM. \n" \
            "Он должен находиться в виде md5-хэша в LASTFM_LOGIN_HASH в .env \n" \
            "Также он может находиться открыто в LASTFM_PASSWORD в .env\n")
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

ensure_dotenv()

dotenv.load_dotenv()
if os.getenv("COOKIE") == None or os.getenv("COOKIE") == "":
    print("Для более стабильной работы заполните COOKIE в .env!\n")

if (os.getenv("LASTFM_PASSWORD_HASH"), os.getenv("LASTFM_PASSWORD")) != (None, None) and (os.getenv("LASTFM_PASSWORD_HASH"), os.getenv("LASTFM_PASSWORD")) != ("", ""):
    user_data = {"TOKEN_YANDEX":os.getenv("TOKEN_YANDEX") if os.getenv("TOKEN_YANDEX")!=None 
                and os.getenv("TOKEN_YANDEX")!="" else trouble_dotenv("TOKEN_YANDEX"),
                    "TOKEN_LASTFM":os.getenv("TOKEN_LASTFM") if os.getenv("TOKEN_LASTFM")!=None
                and os.getenv("TOKEN_LASTFM")!="" else trouble_dotenv("TOKEN_LASTFM"),
                    "SECRET_LASTFM":os.getenv("SECRET_LASTFM") if os.getenv("SECRET_LASTFM")!=None
                and os.getenv("SECRET_LASTFM") !="" else trouble_dotenv("SECRET_LASTFM"),
                    "LASTFM_LOGIN":os.getenv("LASTFM_LOGIN") if os.getenv("LASTFM_LOGIN")!=None
                and os.getenv("LASTFM_LOGIN")!="" else trouble_dotenv("LASTFM_LOGIN"),
                    "LASTFM_PASSWORD": os.getenv("LASTFM_PASSWORD_HASH") if os.getenv("LASTFM_PASSWORD_HASH")!=None and
                    os.getenv("LASTFM_PASSWORD_HASH")!="" else pylast.md5(os.getenv("LASTFM_PASSWORD")),
                    "COOKIE":os.getenv("COOKIE")}
else:
    trouble_dotenv("PASSWORD")

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

