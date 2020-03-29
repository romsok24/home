#!/bin/sh

PLIK_LOGU="/bck/tmp/ruchsieci_$(date +"%Y_%m_%d").csv"
echo > $PLIK_LOGU

while true;
do
  ssh  admin@10.200.10.18 tail -n1 /proc/net/ip_conntrack | grep -v bytes=0 | grep tcp | awk '{gsub(/(src|dst|sport|dport|bytes|mark)=/, "");print $3","$5","$6","$7","$8","$16}'  >> $PLIK_LOGU
  sleep 1
done
