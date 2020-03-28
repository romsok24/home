ECHO OFF
If EXIST "\\hp\bck\dekk\backup.txt" (
date /t > c:\temp\backup.log  2>&1
time /t >>  c:\temp\backup.log  2>&1


echo "===============Backup w tle when iddle" >> c:\temp\backup.log
echo "===============Kopia x dane  :" >> c:\temp\backup.log
xcopy "x:\dane" g:\dane /Y /D /S /C /F  >> c:\temp\backup.log 2>&1
xcopy "x:\dane_inne\media\zdjecia" g:\zdjecia /Y /D /S /C /F  >> c:\temp\backup.log 2>&1
xcopy "x:\dane_inne\media\muzyka" g:\muzyka /Y /D /S /C /F  >> c:\temp\backup.log 2>&1

echo "===============Kopia C documents  :" >> c:\temp\backup.log
xcopy "c:\Users\rom\Documents" g:\c_doocuments /Y /S /D /C /F  >> c:\temp\backup.log 2>&1
echo "===============Kopia C temp  :" >> c:\temp\backup.log
xcopy "c:\temp" g:\c_temp /Y /S /D /C /F  >> c:\temp\backup.log 2>&1
echo "===============Kopia ntfs.iso  :" >> c:\temp\backup.log
xcopy "C:\Windows\ntfs.iso" g:\ /Y /S /C /F  >> c:\temp\backup.log 2>&1
xcopy C:\Windows\ntfs.iso c:\Users\rom\Desktop\Documents\wymiana\ntfs\   /Y /D /S /C /F  >> c:\temp\backup.log 2>&1




echo "===============Backup w tle when iddle" >> c:\temp\backup.log
echo "===============Kopia x dane  :" >> c:\temp\backup.log
xcopy "x:\dane" \\hp\bck\dekk\dane /Y /D /S /C /F  >> c:\temp\backup.log 2>&1
xcopy "x:\dane_inne\media\zdjecia" \\hp\media /Y /D /S /C /F  >> c:\temp\backup.log 2>&1

REM echo "===============Kopia TB  :" >> c:\temp\backup.log
REM xcopy "C:\Users\rom\AppData\Roaming\Thunderbird" \\hp\bck\dekk\TBprofil /Y /S /D /C /F   >> c:\temp\backup.log 2>&1
echo "===============Kopia C documents  :" >> c:\temp\backup.log
xcopy "c:\Users\rom\Documents" \\hp\bck\dekk\doocuments /Y /S /D /C /F  >> c:\temp\backup.log 2>&1
echo "===============Kopia ntfs.iso  :" >> c:\temp\backup.log
xcopy "C:\Windows\ntfs.iso" \\hp\bck\dekk\doocuments\ /Y /S /C /F  >> c:\temp\backup.log 2>&1
xcopy C:\Windows\ntfs.iso c:\Users\rom\Desktop\Documents\wymiana\ntfs\   /Y /D /S /C /F  >> c:\temp\backup.log 2>&1


echo Backup z dnia %DATE% > \\hp\bck\dekk\backup.txt


echo "===============Koniec backupu o godz.:" >> c:\temp\backup.log
time /t >>  c:\temp\backup.log  2>&1
) else (
echo "===============ERROR: Nie istnieje sciezka do backupu" >> c:\temp\backup.log
time /t >>  c:\temp\backup.log  2>&1
echo "===============ERROR: Koniec skryptu backupu" >> c:\temp\backup.log
)
