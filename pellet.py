# Skrypt monitorujacy poziom pelletu w zasobniku
# Realizacja na podst. monitorowania poziomu na wejsciu GPIO21 rpizero01
# Konfiguracja maili: https://wiki.archlinux.org/title/Msmtp#Server_sent_empty_reply

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
      os.system("printf 'Subject: Sprawdź poziom pelletu\nFrom: Kolownia Sliwice\nSprawdź poziom pelletu w zasobniku. \nZasypu wystarczy tylko na ok 1.5 dnia palenia, liczac od pierwszego komunikatu! \n\n\nAlert został wygenerowany automatycznie - nie odpowiadaj na niego.' | /usr/bin/msmtp  examp1@eample.com")
  sleep(14400)


