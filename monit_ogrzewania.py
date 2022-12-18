#
# Program do szybkiej analizy logów za sterowników ogrzewania TECH
# Generuje kilka wygodnych do analizy plików z najważniejszymi danymi
#
import csv, re, os, shutil
from datetime import datetime
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from pyexcel.cookbook import merge_all_to_a_book
import cfg.monit_ogrzewania as cfg


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


print(f"Przetwarzam plik wejściowy:{bcolors.WARNING} {cfg.infile}{bcolors.ENDC}")
# -------------------------------------------------------------------------------------------------

zjakiej_daty = cfg.zjakiego_dnia + "." + cfg.zjakiego_mca + "." + cfg.zjakiego_roku
today = datetime.now().strftime("%d.%m.%Y")
cfg.katalog_out = os.path.join(
    cfg.katalog_out,
    cfg.zjakiego_roku + "_" + cfg.zjakiego_mca + "_" + cfg.zjakiego_dnia,
)
if not os.path.exists(cfg.katalog_out):
    os.makedirs(cfg.katalog_out, exist_ok=True)
cfg.katalog_out = cfg.katalog_out + "\\"
filterfile = cfg.katalog_out + "filter.csv"
filterfilex = cfg.katalog_out + "filter.xlsx"
alarmfile = cfg.katalog_out + "alarm.csv"
rozpalaniefile = cfg.katalog_out + "2gie_rozpalanie.csv"
plomienfile = cfg.katalog_out + "plomien.csv"
czaspaleniafile = cfg.katalog_out + "czas_palenia.csv"
temperaturafile = cfg.katalog_out + "temperatura_" + cfg.zjakiego_dnia + ".csv"
temppaleniafile = cfg.katalog_out + "temperatura_palenia_" + cfg.zjakiego_dnia + ".csv"


# =================Spr czy pendrive nie jest pełny bo to blokuje sterownik pieca i rozpalanie =================
sciezka = cfg.infile
wolne_miejce = shutil.disk_usage(sciezka)
wolne_miejce = str(wolne_miejce)[:-1].split(sep="=")[-1]
wolne_miejce_mb = str(int(wolne_miejce) // 1024 // 1024)

if int(wolne_miejce_mb) <= 100:
    print(f"Na pendrive jest " + wolne_miejce_mb + " MB wolnego miejsca.")
    print(
        f" {bcolors.WARNING} To powoduje błąd {bcolors.ENDC}rozpalania sterownika pieca. Wyczyść go."
    )
# =============================================================================================================


drugie_rozpalanie = False
wartosc_plomienia = -1
czas_rozpalania = ""
czas_wygaszania = ""

with open(cfg.infile, "r") as fin, open(filterfile, "w") as fout, open(
    alarmfile, "w"
) as falarm, open(rozpalaniefile, "w") as frozp, open(plomienfile, "w") as fplom, open(
    czaspaleniafile, "w"
) as fczaspal, open(
    temperaturafile, "w"
) as ftemperatura, open(
    temppaleniafile, "w"
) as ftemppalenia:
    writer = csv.writer(fout, delimiter=";", lineterminator="\n")
    writer_arlam = csv.writer(falarm, delimiter=";", lineterminator="\n")
    writer_rozp = csv.writer(frozp, delimiter=";", lineterminator="\n")
    writer_plom = csv.writer(fplom, delimiter=";", lineterminator="\n")
    writer_czaspalenia = csv.writer(fczaspal, delimiter=";", lineterminator="\n")
    writer_temperatura = csv.writer(ftemperatura, delimiter=";", lineterminator="\n")
    writer_temppalenia = csv.writer(ftemppalenia, delimiter=";", lineterminator="\n")

    writer_plom.writerow("data;godz;wentylator;plomien".split(";"))
    writer.writerow("data;godz;opis;plomien".split(";"))
    writer_temperatura.writerow(
        ("Wykres temperatur z dnia " + zjakiej_daty + ";").split(";")
    )
    writer_temperatura.writerow(
        (
            "godz;temp CO "
            + cfg.zjakiego_dnia
            + ";temp CWU "
            + cfg.zjakiego_dnia
            + ";czy pompa"
        ).split(";")
    )
    writer_temppalenia.writerow(
        ("Wykres temperatur z dnia " + zjakiej_daty + " (za czas palenia);").split(";")
    )
    writer_temppalenia.writerow(
        (
            "godz;temp CO "
            + cfg.zjakiego_dnia
            + ";temp CWU "
            + cfg.zjakiego_dnia
            + ";czy pompa"
        ).split(";")
    )

    for row in csv.reader(fin, delimiter=";"):
        if len(row) > 2:
            # print(row)
            if len(row) > 4:
                if (
                    row[1].strip() == "1"
                    and row[2].strip() == "0"
                    and re.match(".?\d+$", row[4].strip(), flags=0)
                ):
                    if len(row) > 9:
                        row = row[0].split("_") + row
                        row2 = (
                            row[0]
                            + ";"
                            + row[1]
                            + ";"
                            + row[10].strip()
                            + ";"
                            + row[12].strip()
                        )
                        writer_plom.writerow(row2.split(";"))
                        wartosc_plomienia = row[12].strip()

            if (
                row[2].strip() == "1"
                and len(row) > 4
                and not re.match(".*zapisane spaliny.*", row[3].strip(), flags=0)
            ):  # 1 w row[2] oznacza tekst: if not re.match(".?\d+$", row[3].strip(), flags=0):
                # print(row)
                row2 = row[0].split("_") + row
                del row2[2:5]
                row2.pop()
                row2.extend([wartosc_plomienia])
                row2[2] = row2[2].replace("=", " --> ")
                writer.writerow(row2)

            if row[1].strip() == "2" and row[5].strip() > "0":
                row = row[0].split("_") + row
                row2 = (
                    row[1]
                    + ";"
                    + str((int(row[5].strip()) / 10)).replace(".", ",")
                    + ";"
                    + str((int(row[7].strip()) / 10)).replace(".", ",")
                    + ";"
                    + (row[15])
                )
                writer_temperatura.writerow(row2.split(";"))

                if czas_rozpalania != "":
                    writer_temppalenia.writerow(row2.split(";"))

            if len(row) > 4:
                if re.match(".*alarm.*", row[4].strip(), flags=0):
                    writer_arlam.writerow(row)

            if re.match(
                ".*rozpalanie state on exit.*", row[3].strip(), flags=0
            ) or re.match(".*wygaszanie state on exit.*", row[3].strip(), flags=0):
                czas_fmt = "%Y-%m-%d_%H:%M:%S"
                row3 = row[0] + ";" + row[3]

                czas = row3.split(";")[0]
                opis = row3.split(";")[1]
                opis = opis.replace("rozpalanie state on exit", "rozpalenie")
                opis = opis.replace("wygaszanie state on exit", "wygaszenie")
                writer_czaspalenia.writerow((czas + ";" + opis).split(";"))

                if re.match(".*rozpalenie.*", opis, flags=0):
                    czas_rozpalania = datetime.strptime(czas, czas_fmt)
                if re.match(".*wygaszenie.*", opis, flags=0):
                    czas_wygaszania = datetime.strptime(czas, czas_fmt)
                    czas_palenia_min = (
                        czas_wygaszania - czas_rozpalania
                    ).total_seconds() / 60.0
                    czas_palenia_h = (
                        (czas_wygaszania - czas_rozpalania).total_seconds()
                        / 60.0
                        / 60.0
                    )
                    # czas_palenia_h_reszta =  (round(czas_palenia_h) * 60) - czas_palenia_min
                    writer_czaspalenia.writerow(
                        ("Czas palenia [min]:" + str(round(czas_palenia_min))).split(
                            ";"
                        )
                    )
                    writer_czaspalenia.writerow(
                        (
                            "Czas palenia: ok " + str(round(czas_palenia_h, 1)) + "h "
                        ).split(";")
                    )
                    czas_rozpalania = ""
                    czas_wygaszania = ""

            if len(row) > 4:
                if re.match(".*zabezpieczenie grzalki.*", row[4].strip(), flags=0):
                    drugie_rozpalanie = True
                    row2 = "data;godz;wentylator;plomien"
                    writer_rozp.writerow(row2.split(";"))

            if (
                drugie_rozpalanie == True
                and row[1].strip() == "1"
                and row[2].strip() == "0"
                and re.match(".?\d+$", row[4].strip(), flags=0)
            ):
                if len(row) > 9:
                    row = row[0].split("_") + row
                    row2 = row[0] + ";" + row[1] + ";" + row[10] + ";" + row[12]
                    writer_rozp.writerow(row2.split(";"))

df = pd.read_csv(filterfile, delimiter=";", lineterminator="\n")

print(f"Wygenerowałem pliki pomocnicze w katalogu: {cfg.katalog_out}")
# df = df.sort_values(by=['godz','plomien\r'])
# plt.scatter( x = 'godz', y = 'plomien\r', label= "stars", color= "green",marker= "*", s=30)
# plt.show()


# fig = px.line(df, x = 'godz', y = 'plomien\r', title='Natężenie płomienia', markers=True)
# plt.ylim(1,8)
# fig.show()
