import network, time, urequests
from machine import Pin, ADC

sensor = ADC(Pin(36))

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

if conectaWifi ("RedMiHugo", "Hupe6493"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    url = "https://api.thingspeak.com/update?api_key=TNLG4J6M5WA37Y01"
    
    while True:
        
        lectura = sensor.read_u16()
        print("Lectura = {}".format (lectura))
        respuesta = urequests.get(url+"&field1="+str(lectura))
        print(respuesta.text)
        print (respuesta.status_code)
        respuesta.close ()
        time.sleep(2)
   
  
else:
       print ("Imposible conectar")
       miRed.active (False)