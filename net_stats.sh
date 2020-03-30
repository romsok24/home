#!/bin/bash

#IFACES="$(cat /dane/net_ifaces | ssh -T admin@10.***.***.*** )"
RXTX="$(cat /dane/net_rxtx | ssh -T admin@10.***.***.***)"

printf  "Statystyki uzycia sieci na ASUS\n"
#echo "interface RX[GB]  TX[GB]" | column -t
#paste <(printf %s "$IFACES") <(printf %s "$RXTX") | grep -v "0 \[B"  | column -t #| awk '{if ($5=="MiB") print $4/1024 else print $4}' | column -t
echo -e "interface RX[GB] TX[GB] SUM[GB]\n$RXTX" | column -t


echo
#echo $( ssh admin@10.200.10.18 uptime)
