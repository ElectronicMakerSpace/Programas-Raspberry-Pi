import os, socket, time
from urllib.parse import urlencode
from urllib.request import Request,urlopen
#from urlparse import urlparse
from pynput import keyboard
import RPi.GPIO as GPIO

#pip install pynput

contador = 0 
matriz = []
matriz_2 = []

ledPinG = 12
ledPinR = 11
ledPinB = 13

delay = 1
numero = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(ledPinR, GPIO.OUT)
GPIO.setup(ledPinG, GPIO.OUT)
GPIO.setup(ledPinB, GPIO.OUT)

post_fields = {'ID': 3, 'nparte': 12345678910}
url = 'http://bi.agelectronica.com/botonera/scanner.php'
RemoteServer = "www.google.com"


def ethernet():
    try:
        host = socket.gethostbyname(RemoteServer)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        #pass
        return False

def on_press(key):
    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        #print(matriz)
        if (len(matriz) <= 11):
            matriz.append(key.char)
            #print(matriz)
            #print("Tam Matriz: {0}".format(len(matriz)))
            if (len(matriz) == 11):
                #del matriz[:]
                return False
       
    except AttributeError:
        #print('special key {0} pressed'.format(key))   
        return False     

#with keyboard.Listener(on_press=on_press) as listener:
#    listener.join()

# ...or, in a non-blocking fashion:

time.sleep(2)

while True:
    time.sleep(1)
    print("Empieza")
    if (ethernet()):
        print("Conexion Exitosa")
        GPIO.output(ledPinG, GPIO.HIGH)
        GPIO.output(ledPinR, GPIO.LOW) 
        if (len(matriz) == 0 ):
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
            listener = keyboard.Listener(on_press=on_press)
            #listener.start()
        elif(len(matriz) == 11 ):
            #Join de los datos de la lista
            #print('matriz principal',matriz)
            cadena = ''.join(matriz)

            #Envio de Informacion a la pagina
            post_fields['nparte'] = cadena
            request = Request(url, urlencode(post_fields).encode())
            json = urlopen(request).read().decode()
            #print('matriz en cadena',cadena)
            #print('Tam de la cadena {0}'.format(len(cadena)))       
            del matriz[:]
            #print('matriz borrada',matriz)
    else:
        print('Sin conexion a Internet, porfavor revise')
        GPIO.output(ledPinR, GPIO.HIGH)
        GPIO.output(ledPinG, GPIO.LOW)
