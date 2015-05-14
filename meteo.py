from ubidots import ApiClient
from time import sleep
from grove_i2c_barometric_sensor import BMP085
import grovepi

lum_pin = 0
DHT_pin = 3
pir_pin = 8
relay_pin = 2

bmp = BMP085(0x77, 1)

grovepi.pinMode(pir_pin, "INPUT")
grovepi.pinMode(relay_pin, "OUTPUT")
#Create an "API" object

api = ApiClient("Your api client")

#Create a "Variable" object

lum = api.get_variable("variable id")
temp = api.get_variable("variable id")
hum = api.get_variable("variable id")
pres = api.get_variable("variable id")

while True:
    try:
        # Retrieve data
        [T,H] = grovepi.dht(DHT_pin, 1)
        P = bmp.readPressure()
        L = grovepi.analogRead(lum_pin)

        # test and send data
        if T < 100 and H < 100 :
            print T
            print H
            temp.save_value({'value': T})
            hum.save_value({'value': H})
        if L <= 1024 :
            lum.save_value({'value': L})
        if P < 200000 :
            print P
            pres.save_value({'value': P/100})
        
        # 5 min delay
        sleep(300)
    except IOError:
        print "Erreur: IO"
    except TypeError:
        print "Erreur: Type"
    except KeyboardInterrupt:
        print "Programme interrompu"
        break
