# Skrypt monitorujacy poziom pelletu w zasobniku
# Realizacja na podst. monitorowania poziomu na wejsciu GPIO21 rpizero01

import RPi.GPIO as GPIO, os
from time import *
from datetime import date, datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
sleep(60)

while True:
  dateczka=datetime.now().strftime("%d %b, %H:%M")
  if(GPIO.input(21) == 0):
      print('Uwaga - sprawdz poziom pelletu w zasobniku! Stan na dzien {dateczka}'.format(dateczka=dateczka))
      os.system("/bin/echo -e 'Sprawdz poziom pelletu w zasobniku. \nZasypu wystarczy tylko na ok 1.5 dnia palenia, liczac od pierwszego komunikatu! \n\n\nAlert zostal wygenerowany automatycznie - nie odpowiadaj na niego.' | /usr/bin/mailx -s 'Sprawdz poziom pelletu' examp1@eample.com -a 'From: Kotlownia *****'")
      os.system("/bin/echo -e 'Sprawdz poziom pelletu w zasobniku. \nZasypu wystarczy tylko na ok 1.5 dnia palenia, liczac od pierwszego komunikatu! \n\n\nAlert zostal wygenerowany automatycznie - nie odpowiadaj na niego.' | /usr/bin/mailx -s 'Sprawdz poziom pelletu' examp2@eample.com -a 'From: Kotlownia *****'")
      os.system("/bin/echo -e 'Sprawdz poziom pelletu w zasobniku. \nZasypu wystarczy tylko na ok 1.5 dnia palenia, liczac od pierwszego komunikatu! \n\n\nAlert zostal wygenerowany automatycznie - nie odpowiadaj na niego.' | /usr/bin/mailx -s 'Sprawdz poziom pelletu' examp3@eample.com -a 'From: Kotlownia *****'") 
  sleep(14400)


