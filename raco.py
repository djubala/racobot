import requests
import json
from os import remove

global db

def descarga_imagen(img, url):
    r = requests.get(url, allow_redirects=True)
    open(img, 'wb').write(r.content)

def borrar_imagen(img):
    remove(img)

def init_db():
    f = open('db.json', 'r')
    dbaux = f.read()
    f.close()
    db = json.loads(dbaux)
    
init_db()