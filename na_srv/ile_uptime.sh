#!/bin/bash
ile=$(ssh  admin@10.***.***.*** uptime | awk '{print $3}' | sed 's/,//' |  sed 's/://')
jednostka=$(ssh  admin@10.***.***.*** uptime | awk '{print $4'} | sed 's/,//')
echo "Router pracuje od $ile$jednostka"
if (( $ile < 4 )); then 
  if [ "$jednostka" = "min" ]; then
    if [ ! -f /tmp/byl_restart_asusa ]; then
      touch /tmp/byl_restart_asusa
      echo "Wykryto restart routera $ile min. temu"
      echo "Subject: Wykryto restart routera $ile min. temu" | /usr/sbin/ssmtp examp1@eample.com
      sleep 240 &&
      ssh  admin@10.***.***.*** ip r add default via  10.***.***.***
      rm -f /tmp/byl_restart_asusa
    fi
  fi
fi
