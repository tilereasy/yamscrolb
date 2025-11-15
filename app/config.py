import json, os, threading
from pathlib import Path

CONFIG_PATH = Path(os.environ.get("CONFIG_PATH", "/data/config.json"))
_lock = threading.RLock()

DEFAULTS = {
    "TOKEN_YANDEX": None,
    "TOKEN_LASTFM": None,
    "SECRET_LASTFM": None,
    "LASTFM_LOGIN": None,
    "LASTFM_PASSWORD_HASH": None,
    "LASTFM_PASSWORD": None,
    "COOKIE": None,
    "SCROBBLE_COOLDOWN": int(os.environ.get("SCROBBLE_COOLDOWN", "15")),
    "FULLMODELSCOUNT": int(os.environ.get("FULLMODELSCOUNT", "2")),
}

def load_config():
    with _lock:
        cfg = DEFAULTS.copy()
        for key in DEFAULTS:
            value = os.environ.get(key)
            if value:
                cfg[key] = value
        if CONFIG_PATH.exists():
            try:
                data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
                for key, value in data.items():
                    if value is not None:
                        cfg[key] = value
            except:
                pass
        return cfg
    
def save_config(new_cfg):
    with _lock:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(new_cfg, ensure_ascii=False), encoding="urf-8")
    