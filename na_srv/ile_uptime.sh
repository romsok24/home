#!/bin/bash
ile=$(ssh  admin@10.200.10.18 uptime | awk '{print $3}' | sed 's/,//' |  sed 's/://')
jednostka=$(ssh  admin@10.200.10.18 uptime | awk '{print $4'} | sed 's/,//')
echo "Router pracuje od $ile$jednostka"
if (( $ile < 4 )); then 
  if [ "$jednostka" = "min" ]; then
    if [ ! -f /tmp/byl_restart_asusa ]; then
      touch /tmp/byl_restart_asusa
      echo "Wykryto restart routera $ile min. temu"
      echo "Subject: Wykryto restart routera $ile min. temu" | /usr/sbin/ssmtp 24roman12kam1@gmail.com
      sleep 240 &&
      ssh  admin@10.200.10.18 ip r add default via  10.200.10.17
      rm -f /tmp/byl_restart_asusa
    fi
  fi
fi
