from .models import Data
import csv

with open('data/files/vektlofting_norge.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        data_row = Data(
                idx         = row[0],
                lofter      = row[1],
                fodt        = row[2],
                aar         = row[3],
                mnd         = row[4],
                dag         = row[5],
                vekt        = row[6],
                kat         = row[7],
                rykk        = row[8],
                stot        = row[9],
                sml         = row[10],
                sinclair    = row[11],
                tau         = row[12],
                klubb       = row[13],
                stevne      = row[14]
                )
        data_row.save()


def replace_chars():
    d = Data.objects.all()
    for entry in d:
        correct_charset_1 = entry.klubb.encode("windows-1252").decode("utf-8")
        correct_charset_2 = entry.stevne.encode("windows-1252").decode("utf-8")
        entry.klubb = correct_charset_1
        entry.stevne = correct_charset_2
        entry.save()