#!/bin/bash

ZDJECIA=/home/ftptransfer/kamera/*.jpg

licznik=0
echo "Przed: " `ls -l $ZDJECIA | wc -l`
for plik in $ZDJECIA
do
	if [ $licznik -eq 0 ]; then 
		wzorzec=$plik
		echo "Wzorzec: $wzorzec" 
	else
		echo "Przetwarzam plik $plik ...."
		wynik_por=$(compare -quiet -metric RMSE $wzorzec $plik nic.tmp 2>&1 | head -n1 | cut -d" " -f1 | cut -d "." -f1)
		echo "Wynik: $wynik_por"
		if [ $wynik_por -lt 2000 ]; then
			echo "Usuwam: $plik" 
			rm -f $plik 
		else
			nowanazwa=$plik."_wys"
			#echo "Wykryto ruch" | mutt -s "Ruch z kamery (Cam1)" -a $plik -- 24roman12kam1@gmail.com
			mv $plik $nowanazwa
		fi
	fi
	licznik=$((licznik+1))
	if [ $licznik -eq 2 ]; then
		licznik=0	
 		nowanazwa=$wzorzec."_wys"
		#echo "Wykryto ruch" | mutt -s "Ruch z kamery (Cam1)" -a $wzorzec-- 24roman12kam1@gmail.com
                mv $wzorzec $nowanazwa
	fi
	echo -e "\n"
done
if [ $licznik -eq 1 ]; then
	nowanazwa=$wzorzec."_wys"
        #echo "Wykryto ruch" | mutt -s "Ruch z kamery (Cam1)" -a $plik -- 24roman12kam1@gmail.com
        mv $plik $nowanazwa
fi
echo "Po: " `ls -l $ZDJECIA | wc -l`
