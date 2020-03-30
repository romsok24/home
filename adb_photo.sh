#!/bin/bash

# robi zdj leokalnie co minute ale wysyla na Google co 5min aby zaosczedzic pasmo 

cat /dev/null > /tmp/adb_photo.log
exec > /tmp/adb_photo.log
exec 2>&1

zdj_aparat=/mnt/shell/emulated/0/DCIM/Camera
zdj_aparat_folder=$(basename $zdj_aparat)

date
#echo "Instaluje rclone..."
#curl https://rclone.org/install.sh | sudo bash
#rclone config

echo "Usuwam stare pliki z gdrive..."
for idel in $(/usr/bin/rclone ls GDrive:/kamera/  | grep kociol | awk '{print $2}');do /usr/bin/rclone deletefile GDrive:/kamera/$idel;done
licznik=1

echo "Odblokowanie telefonu"
adb devices
#adb shell "am start -a android.intent.action.CALL -d tel:6951018"
sleep 5

echo "Robi zdjecia telefonem, sciaga loaklnie, kasuje na telefoniei i w chmurze"
while true
do
  date
  bateryjka=$(adb shell dumpsys battery | grep level)
  echo "Bateria: $bateryjka"
  czy_brak_dev=$(adb devices)
  if [[ $czy_brak_dev == *"no"* ]]; then
   /bin/echo -e 'Nie znaleziono telefonu podlaczonego do maliny PiZero w kotlowni! \n\n\nAlert zostal wygenerowany automatycznie - nie odpowiadaj na niego.' | /usr/bin/mailx -s 'Tel odlaczony od PiZero' *****@***** -a 'From: Kotlownia ******' 
  fi
  adb shell "am start -W -c android.intent.category.HOME -a android.intent.action.MAIN"
  adb shell "am start -a android.media.action.IMAGE_CAPTURE"
  sleep 2
  adb shell "input keyevent 27"
  sleep 2
  adb shell "am start -W -c android.intent.category.HOME -a android.intent.action.MAIN"
  echo "Pobieram zdj z telefonu..."
  adb pull $zdj_aparat /kamery/
  mv /kamery/$zdj_aparat_folder/* /kamery/kociol/
  echo "Plikow w katalogu:"
  ls -tp /kamery/kociol/ | grep -v '/$' | wc -l
  echo "Do usuniecia:"
  ls -tp /kamery/kociol/ | grep -v '/$' | tail -n +2 | wc -l
  echo
  for pliczek in $(ls -l /kamery/kociol/ | grep jpg | awk '{print $9;}');do adb shell rm $zdj_aparat/$pliczek;done;
  ls -tp /kamery/kociol/*  | grep -v '/$'  | tail -n +2  | xargs -I {} rm -f -- {}
  for pliczek in $(ls -l /kamery/kociol/ | grep jpg | awk '{print $9;}');do cp /kamery/kociol/$pliczek /kamery/kociol/kociol.jpg;done;
  adb shell am start -W -c android.intent.category.HOME -a android.intent.action.MAIN
  if [ "$licznik" -eq 5 ] ; then
    echo "Restartuje telefon..."
    adb reboot
    sleep 30
    stary_kocio=$(/usr/bin/rclone ls GDrive:/kamera/  | grep kociol | awk '{print $2}')
    echo "Kasuje stary kociol.jpg ( $stary_kocio )z g-drive..."
    /usr/bin/rclone deletefile GDrive:$stary_kocio
    echo "Wysylam na g-drive..."
    /usr/bin/rclone copy /kamery/kociol/kociol.jpg GDrive:/kamera/
    licznik=1
    echo "Licznik znow na $licznik"
  else
    echo "Licznik $licznik"
    licznik=$((licznik+1))
  fi 
  echo "A teraz spie min...."
  sleep 60
  # adb shell "am start -a android.intent.action.CALL -d tel:69510178"
  if [ $(/usr/bin/rclone ls GDrive:/kamera/  | grep kociol | wc -l) -gt 20 ]; then 
    echo "Duzo plikow kociol.jpg w chmurze - kasuje..."
    for ide in $(/usr/bin/rclone ls GDrive:/kamera/  | grep kociol | awk '{print $2}');do /usr/bin/rclone deletefile GDrive:/kamera/$idel;done
  fi
  sleep 4 
done
 
