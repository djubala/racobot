import requests
import json
from datetime import datetime, date
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
    

cliente = 'client_id=zN7ikID1R4aBfNIhZ0tgFogSXKdF348NnXzFbl6F'
def aules_disponibles(aula):
    response = requests.get('https://api.fib.upc.edu/v2/laboratoris/?'+cliente,headers={'accept': 'application/json'})
    result = response.json()
    for a in result["results"]:
        if len(a["reserves_actuals"]) == 0 and a["places_disponibles"] is not None and a["places_disponibles"]>0:
            print(a["id"]+" : "+str(a["places_disponibles"]))
    #print(rJson["imatges"]["B5"])
    

def reservar(aula, data_fi):
    today = date.today()
    timeF = today.strftime("%Y-%m-%d")
    print(timeF)
    actMin =  datetime.now().hour*60 +datetime.now().minute
    actMin = 540
    print(datetime.now().hour)
    print(datetime.now().minute)
    response = requests.get('https://api.fib.upc.edu/v2/laboratoris/reserves/?page=16&'+cliente, headers={'accept': 'application/json'})
    result = response.json()
    for a in result["results"]:
        if a["laboratori"].lower() == aula.lower():
            if (a["inici"].lower()).startswith("2019-10-15"):#Depende del array de las reservas de hoy, esto quizas no sea necesario
                iniAux = (a["inici"][11:]).split(":")
                fiAux = (a["fi"][11:]).split(":")
                resAux = data_fi.split(":")
                iniMin = int(iniAux[0])*60+int(iniAux[1])
                fiMin = int(fiAux[0])*60+int(fiAux[1])
                resMin = int(resAux[0])*60+int(resAux[1])
                aMax = max(iniMin,actMin)
                bMin = min(fiMin, resMin)
                if aMax <= bMin:
                    print(a["id"])
                    return [False, a["titol"]]
    
    return [True,""]


#init_db()
