# - *- coding: utf- 8 - *-
# Skrypt monitorujacy poziom pelletu w zasobniku
# Realizacja na podst. monitorowania poziomu na wejsciu GPIO21 rpizero01
# Konfiguracja maili: https://wiki.archlinux.org/title/Msmtp#Server_sent_empty_reply

import RPi.GPIO as GPIO, os
from time import *
from datetime import date, datetime
import os

def include(filename):
    if os.path.exists(filename):
        execfile(filename)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
print('Czekam na rozpoczęcie....')
sleep(60)

while True:
  dateczka=datetime.now().strftime("%d %b, %H:%M")
  if(GPIO.input(21) == 0):
       include(open('/home/pi/dane/mail.py').read())
  print('Czekam 4h do następnego sprawdzenia...')
  sleep(14400)
  
