import requests
import json
from datetime import datetime, date
from os import remove

global db
cliente = 'client_id=zN7ikID1R4aBfNIhZ0tgFogSXKdF348NnXzFbl6F'

def descarga_imagen(img, url):
    r = requests.get(url, allow_redirects=True)
    open(img, 'wb').write(r.content)

def borrar_imagen(img):
    remove(img)

def init_db():
    f = open('db.json', 'r')
    dbaux = f.read()
    f.close()
    global db
    db = json.loads(dbaux)
    
def aules_disponibles(edificio, filtrar):
    response = requests.get('https://api.fib.upc.edu/v2/laboratoris/?'+cliente,headers={'accept': 'application/json'})
    result = response.json()
    lista_aulas = []
    for a in result["results"]:
        if len(a["reserves_actuals"]) == 0 and a["places_disponibles"] is not None and a["places_disponibles"]>0:
            if filtrar is not None:
                if (a["id"].lower()) in filtrar:
                    if edificio is not None:
                        if (a["id"].lower()).startswith(edificio.lower()):
                            aux = []
                            aux.append(a["id"])
                            aux.append(a["places_disponibles"])
                            lista_aulas.append(aux)
                    else:
                        aux = []
                        aux.append(a["id"])
                        aux.append(a["places_disponibles"])
                        lista_aulas.append(aux)
  
            else:
                if edificio is not None:
                    if (a["id"].lower()).startswith(edificio.lower()):
                        aux = []
                        aux.append(a["id"])
                        aux.append(a["places_disponibles"])
                        lista_aulas.append(aux)
                else:
                    aux = []
                    aux.append(a["id"])
                    aux.append(a["places_disponibles"])
                    lista_aulas.append(aux)
    return lista_aulas
    #print(rJson["imatges"]["B5"])
    

def reservar(aula, data_fi):
    today = date.today()
    timeF = today.strftime("%Y-%m-%d")
    print(timeF)
    actMin =  datetime.now().hour*60 +datetime.now().minute
    print(datetime.now().hour)
    print(datetime.now().minute)
    response = requests.get('https://api.fib.upc.edu/v2/laboratoris/reserves/?page=16&'+cliente, headers={'accept': 'application/json'})
    result = response.json()
    for a in result["results"]:
        if a["laboratori"].lower() == aula.lower():
            if (a["inici"].lower()).startswith(timeF):#Depende del array de las reservas de hoy, esto quizas no sea necesario
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

def filtrar_aulas(filtros, valores, edificio):
    try:
        aulas = []
        iaulas = []
        
        if edificio is None:
            for e in db:
                for a in db[e]:
                    aulas.append(a);
                    iaulas.append(db[e][a])
        else:
            for a in db[edificio]:
                aulas.append(a);
                iaulas.append(db[edificio][a])
        
        next_aulas = []
        next_iaulas = []
        for f in range(0, len(filtros)):
            for i in range(0, len(aulas)):
                if iaulas[i][filtros[f]] == valores[f]:
                    next_aulas.append(aulas[i])
                    next_iaulas.append(iaulas[i])
            aulas = next_aulas
            iaulas = next_iaulas
            next_aulas = []
            next_iaulas = []
        return aulas
    except Exception as e:
        raise ValueError('El filtro ' + filtros[f] + ' no es valido')

def lista_edi():
    try:
        listaAux = []
        global db  
        for a in db:
            listaAux.append(a)
        return listaAux
    except Exception as e:
        print(e)
        raise ValueError('No se ha podido leer los edificios correctamente')

init_db()
aules_disponibles("a","a")
