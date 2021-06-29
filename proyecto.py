import sys, requests, json, time, os, socket
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from gpiozero import LED

#sudo python proyecto.py
#@reboot sleep 45; sudo python /home/pi/proyecto.py >> /home/pi/Desktop/scanner.log

post_fields = {'ID': 3, 'nparte': 12345678910}
url = 'http://bi.agelectronica.com/botonera/scanner.php'
RemoteServer = "www.google.com"

contador = 0 
matriz = []
codigo_bar = ''

red = LED(17)
green = LED(18)
blue = LED(27)
delay = .5

def scanner():
    try:
        fp = open('/dev/hidraw3', 'rb')
        print("conectado")
        return True  
    except:
        print("conectar")
        return False
    
def envio_informacion(codigo_bar):
    try:
        post_fields['nparte'] = codigo_bar
        request = Request(url, urlencode(post_fields).encode())
        json = urlopen(request).read().decode()
        print('codigo_bar: {0}, Enviado'.format(codigo_bar))
        green.on()
        red.on()
        blue.on()
        time.sleep(delay)
        green.off()
        red.off()
        blue.off()
        #print('matriz en cadena',cadena)
        #print('Tam de la cadena {0}'.format(len(cadena)))
    except:
        #pass
        return False
    

def ethernet():
    try:
        host = socket.gethostbyname(RemoteServer)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        #pass
        return False

def barcode_reader(codigo_bar):
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

    fp = open('/dev/hidraw3','rb')

    ss = ""
    shift = False

    done = False

    while not done:
        ## Get the character from the HID
        buffer = fp.read(8)
        for c in buffer:
            if c > 0:
                ##  40 is carriage return which signifies
                ##  we are done looking for characters
                if int(c) == 40:
                    done = True
                    break

                ##  If we are shifted then we have to
                ##  use the hid2 characters.
                if shift:

                    ## If it is a '2' then it is the shift key
                    if int(c) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid2[int(c)]
                        shift = False

                ##  If we are not shifted then use
                ##  the hid characters

                else:

                    ## If it is a '2' then it is the shift key
                    if int(c) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid[int(c)]

        if (len(codigo_bar) <= 11):
            codigo_bar = ss
            #print(codigo_bar)
            #print("Tam Matriz: {0}".format(len(codigo_bar)))
            if (len(codigo_bar) == 11):
                #del matriz[:]
                envio_informacion(codigo_bar)
                return False
        
    #return ss

while True:
    time.sleep(1)
    if (ethernet()):
        print("Conexion Exitosa")
        red.off()
        blue.off()
        
        green.on()
        #if (len(codigo_bar) == 0 ):
        while True:
            if (scanner()):
                print('Exitosa')
                red.off()
                blue.off()
                
                green.on()
                barcode_reader(codigo_bar)
                if (ethernet() !=True ):
                    break
                else:
                    pass
            if (scanner()!=True):
                print('desconectado')
                green.off()
                blue.off()
                
                red.on()
                time.sleep(delay)
                red.off()
                time.sleep(delay)
                if (ethernet() !=True ):
                    break
                else:
                    pass
                
    else:        
        print('Sin conexion a Internet, o sin scanner')
        green.off()
        blue.off()
        
        red.on()
        time.sleep(delay)
        red.off()
        time.sleep(delay)
