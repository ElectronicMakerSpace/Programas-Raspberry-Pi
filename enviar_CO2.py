from urllib.parse import urlencode
from urllib.request import Request,urlopen
#from urlparse import urlparse

campos = {'equipo': 1, 'valor': -100}

def send_data(equipo, valor):
    # Aqui coloca tus variables 
    campos['equipo'] = equipo
    campos['valor'] = valor

    endpoint = f"https://www.agelectronica.lat/co2/server.php?usuario=Oscar_Benji&equipo={campos['equipo']}&valor={campos['valor']}"
    request = Request(endpoint, urlencode(campos).encode())
    json = urlopen(request).read().decode()
    
    return json
    
response = send_data(11, 777)

print(response)

