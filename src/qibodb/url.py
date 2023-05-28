import urllib.parse
from pathlib import Path

from sqlalchemy import URL


def password(pwd: str):
    return urllib.parse.quote_plus(pwd)


HOST = "localhost"
PORT = 9160
USER = "qibo"
PASSWORD = password("qibopwd")
DEFAULTS = dict(host=HOST, port=PORT, username=USER, password=PASSWORD)


def sqlite(path: Path, **kwargs):
    withdefaults = DEFAULTS.copy()
    withdefaults.update(kwargs)
    return URL.create("sqlite", database=str(path.absolute()), **withdefaults)


def postgres(name: str, **kwargs):
    withdefaults = DEFAULTS.copy()
    withdefaults.update(kwargs)
    return URL.create("postgresql", database=name, **withdefaults)
