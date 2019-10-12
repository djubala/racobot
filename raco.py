import requests
import json

def capacitat():
    response = requests.get('https://api.fib.upc.edu/v2/laboratoris/?format=json&client_id=zN7ikID1R4aBfNIhZ0tgFogSXKdF348NnXzFbl6F')
    labs = json.loads(str(response.content))
    