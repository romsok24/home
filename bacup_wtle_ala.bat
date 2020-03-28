ECHO OFF
If EXIST "\\hp\bck Ala\backup.txt" (
date /t > c:\temp\backup.log  2>&1
time /t >>  c:\temp\backup.log  2>&1


echo "===============Kopia C documents  :" >> c:\temp\backup.log
xcopy "c:\Users\Ala\Documents" g:\c_doocuments /Y /S /D /C /F  >> c:\temp\backup.log 2>&1

echo Backup z dnia %DATE% > \\hp\bck Ala\backup.txt


echo "===============Koniec backupu o godz.:" >> c:\temp\backup.log
time /t >>  c:\temp\backup.log  2>&1
) else (
echo "===============ERROR: Nie istnieje sciezka do backupu" >> c:\temp\backup.log
time /t >>  c:\temp\backup.log  2>&1
echo "===============ERROR: Koniec skryptu backupu" >> c:\temp\backup.log
)
