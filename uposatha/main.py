"""
Parses Uposatha dates from a text file where each line has the format:

<Month> <Day> <Day>* <Day>
"""

import csv

from datetime import date
from datetime import datetime

IN_FILE_PATH = "./dates.txt"
OUT_FILE_PATH = "./out.csv"
YEAR = 2024
EVENT_DESCRIPTION = "Buddhist day of observance. Dates gathered from Metta Forest Monastery: https://www.watmetta.org/"

all_dates = []
with open(IN_FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
    r = csv.reader(file)
    for row in r:
        if not len(row) == 1:
            continue

        original_date = row[0]
        items = original_date.split(" ")
        month = datetime.strptime(items[0], "%B").month
        days = [item.replace("*", "") for item in items[1:]]
        dates = [date(YEAR, month, int(day)).strftime("%m/%d/%Y") for day in days]
        all_dates.extend(dates)

with open(OUT_FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
    w = csv.writer(file)
    date_rows = [["Subject", "Start Date", "All Day Event", "Description"]]
    for date in all_dates:
        date_rows.append(["Uposatha", date, True, EVENT_DESCRIPTION])

    for row in date_rows:
        w.writerow(row)
