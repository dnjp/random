"""
Parses Uposatha dates from a text file where each line has the format:

<Month> <Day> <Day>* <Day>
"""

import csv

from datetime import date
from datetime import datetime

YEAR = 2024

IN_FILE_PATH = "./uposatha/dates.txt"
ALL_DATES_FILE_PATH = "./uposatha/dates.csv"
UPOSATHA_FILE_PATH = "./uposatha/uposatha.csv"
ROW_FORMAT = ["Subject", "Start Date", "All Day Event", "Description"]

UPOSATHA_DESCRIPTION = "Buddhist day of observance. Dates gathered from Metta Forest Monastery: https://www.watmetta.org/"

SPECIAL_DAYS_FILE_PATH = "./uposatha/special.csv"
SPECIAL_DAYS = {
    "Magha Puja": {
        "description": """This day, sometimes called "Sangha Day," commemorates the spontaneous assembly of 1,250 arahants in the Buddha's presence. One thousand of the gathered monks had previously achieved Awakening upon hearing the Buddha's delivery of the Fire Sermon; the remaining 250 were followers of the elder monks Ven. Moggallana and Ven. Sariputta. To mark this auspicious gathering, the Buddha delivered the "Ovada-Patimokkha Gatha" (see "A Chanting Guide"), a summary of the main points of the Dhamma, which the Buddha gave to the assembly before sending them out to proclaim the doctrine. [Suggested reading: "Dhamma for Everyone" by Ajaan Lee.]""",
    },
    "Visakha Puja": {
        "description": """This day, sometimes called "Buddha Day," commemorates three key events in the Buddha's life that took place on this full-moon day: his birth, Awakening, and final Unbinding (parinibbana). [Suggested reading: "Visakha Puja" by Ajaan Lee.]""",
    },
    "Asalha Puja": {
        "description": """This day, sometimes called "Dhamma Day," commemorates the Buddha's first discourse, which he gave to the group of five monks with whom he had practiced in the forest for many years. Upon hearing this discourse, one of the monks ( Ven. Kondañña) gained his first glimpse of Nibbana, thus giving birth to the Noble Sangha. The annual Rains retreat (vassa) begins the following day.""",
    },
    "Vassa Begins": {
        "description": """The tradition of ‘Rains Retreat’ was started by the Buddha Himself in the year 588 BCE, where the Lord and 60 bhikkhus – including the elders Kondañña, Bhaddiya, Vappa, Mahānāma and Assaji, as well as Venerable Yasa and his 54 friends – resided in the vicinity of Sarnath near Varanasi. During those 3 months, the venerables learned and practised Dhamma intensively under the direct guidance of the Buddha; at the end of which, all 60 bhikkhus (monks) had attained the highest spiritual fruit of Arahantship.""",
    },
    "Vassa Ends": {
        "description": """This day marks the end of the Rains retreat (vassa). In the following month, the kathina ceremony is held, during which the laity gather to make formal offerings of robe cloth and other requisites to the Sangha.""",
    },
    "Anapanasati Day": {
        "description": """At the end of one rains retreat (vassa), the Buddha was so pleased with the progress of the assembled monks that he encouraged them to extend their retreat for yet another month. On the full-moon day marking the end of that fourth month of retreat, he presented his instructions on mindfulness of breathing (anapanasati), which may be found in the Anapanasati Sutta (MN 118) — The Discourse on Mindfulness of Breathing.""",
    },
}

uposatha_dates = []
special_dates = []
with open(IN_FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
    r = csv.reader(file)

    is_special_date = False
    for row in r:
        if not len(row) == 1:
            is_special_date = True
            continue

        if is_special_date:
            items = row[0].split(": ")
            subject = items[0].casefold().title()
            special_date = items[1].split(" ")
            month = datetime.strptime(special_date[0], "%B").month
            day = int(special_date[1])
            event_date = date(YEAR, month, day).strftime("%m/%d/%Y")
            event = {
                "subject": subject,
                "date": date(YEAR, month, day).strftime("%m/%d/%Y"),
                "description": SPECIAL_DAYS[subject]["description"],
            }
            special_dates.append(event)
        else:
            original_date = row[0]
            items = original_date.split(" ")
            month = datetime.strptime(items[0], "%B").month
            days = [item.replace("*", "") for item in items[1:]]
            dates = [date(YEAR, month, int(day)).strftime("%m/%d/%Y") for day in days]
            uposatha_dates.extend(dates)


uposatha_rows = []
for date in uposatha_dates:
    uposatha_rows.append(["Uposatha", date, True, UPOSATHA_DESCRIPTION])

special_rows = []
for event in special_dates:
    special_rows.append([event["subject"], event["date"], True, event["description"]])

all_rows = []
all_rows.extend(uposatha_rows)
all_rows.extend(special_rows)


def writerows(filepath: str, events: list):
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        w = csv.writer(file)
        rows = [ROW_FORMAT]
        for event in events:
            rows.append(event)
        for row in rows:
            w.writerow(row)


writerows(UPOSATHA_FILE_PATH, uposatha_rows)
writerows(SPECIAL_DAYS_FILE_PATH, special_rows)
writerows(ALL_DATES_FILE_PATH, all_rows)
