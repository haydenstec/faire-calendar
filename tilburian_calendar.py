import csv
from datetime import datetime, timedelta
import math
import sys

# define start date, 380 calendar year, and today's Gregorian date
start_date = datetime(2009, 8, 23)
interval = timedelta(days=380)
today = datetime.now()

if len(sys.argv) > 1:
    try:
        today = datetime.strptime(sys.argv[1], "%B %d, %Y")
    except ValueError:
        print("Invalid date format. Please use 'Month day, year' format (e.g., 'March 19, 2025').")
        sys.exit(1)

# current Tilburian year
tilburian_year = ((today - start_date).days // 380) + 1

# generate cyclical Tilburian year
cycle_count = 0
year_of_the = "Unknown year"
if (((tilburian_year - 1) % 10) == 9): # is watermelon
    cycle_count = tilburian_year // 10 # rounded down integer from 10
    year_of_the = "Watermelon"
else: # is cabbage
    cycle_count = tilburian_year - (tilburian_year // 10)
    year_of_the = "Cabbage"

cycle_year_label = f"{cycle_count} Year of the {year_of_the}"


# start date of the current Tilburian year
tilburian_year_start = start_date + timedelta(days = (tilburian_year - 1) * 380)
end_of_tilburian_year = tilburian_year_start + timedelta(days = 379)

# gregorian calendar years in Tilburian year
start_gregorian_year = tilburian_year_start.year
end_gregorian_year = end_of_tilburian_year.year

# CALCULATING GREGORIAN HOLIDAYS

# calculates easter date given year Y using Gauss' Easter Algorithm
def gaussEaster(Y):
	A = Y % 19
	B = Y % 4
	C = Y % 7
	
	P = math.floor(Y / 100)
	Q = math.floor((13 + 8 * P) / 25)
	M = (15 - Q + P - P // 4) % 30
	N = (4 + P - P // 4) % 7
	D = (19 * A + M) % 30
	E = (2 * B + 4 * C + 6 * D + N) % 7
	days = (22 + D + E)

    # edge cases
	if ((D == 29) and (E == 6)):
		return datetime(Y, 4, 19)  # April 19
	elif ((D == 28) and (E == 6)):
		return datetime(Y, 4, 18)  # April 18
	else:
		if (days > 31):
			return datetime(Y, 4, days - 31) # April
		else:
			return datetime(Y, 3, days) # March

# calculate Easter(s) in Tilburian year
easters_in_tilburian_year = set()
for gregorian_year in range(start_gregorian_year, end_gregorian_year + 1):
    easter_date = gaussEaster(gregorian_year)

    # check if this Easter Sunday falls within the Tilburian year range
    if tilburian_year_start <= easter_date <= end_of_tilburian_year:
        easters_in_tilburian_year.add(easter_date)

# Pentecost
pentecost_dates = []
for easter in easters_in_tilburian_year:
    pentecost = easter + timedelta(days=49)  # 50 days after Easter
    if tilburian_year_start <= pentecost <= end_of_tilburian_year:
        pentecost_dates.append(pentecost)

# Christmas
christmas = datetime(1, 12, 25)

# Christmas Octave (25th December to 1st January)
christmas_octave_start = datetime(1, 12, 25)
christmas_octave_end = datetime(1, 1, 1)

# Feast of St. Januarius
feast_of_st_januarius = datetime(1, 9, 19)
octave_of_gennaro_end = feast_of_st_januarius + timedelta(days=7)
broomsticks_start = feast_of_st_januarius - timedelta(days=9)
broomsticks_end = feast_of_st_januarius - timedelta(days=1)

# DONE CALCULATING GREGORIAN HOLIDAYS

# ASSIGNING FIXED TILBURIAN FESTIVALS

# festivular months
custom_months = [
    {"month_name": "mensis Pauli", "start_day": 1, "end_day": 81},  # day 1 to day 81
    {"month_name": "mensis Iacobi", "start_day": 82, "end_day": 124},  # day 82 to day 124
    {"month_name": "mensis Benedicti", "start_day": 125, "end_day": 167},  # day 125 to day 167
    {"month_name": "mensis Petri", "start_day": 168, "end_day": 295},  # day 168 to day 295
    {"month_name": "mensis vagandi (Roving Month)", "start_day": 296, "end_day": 380},  # day 296 to day 379
]

# DONE ASSIGNING FIXED TILBURIAN FESTIVALS

# map the days to respective months
day_to_month = {}
for month in custom_months:
    for day in range(month['start_day'], month['end_day'] + 1):
        day_to_month[day] = month['month_name']

# generate current Tilburian year
dates = []
for day in range(1, 381):
    tilburian_date = tilburian_year_start + timedelta(days = day - 1)
    formatted_date = tilburian_date.strftime("%A, %B %d, %Y")

    # weekday
    weekday_name = tilburian_date.strftime("%A")
    
    # ADDING FESTIVAL DAYS - higher priority (liturgical) higher up to be first in list
    festival = []

    # Christmas (25th December)
    if tilburian_date.month == christmas.month and tilburian_date.day == christmas.day:
        festival.append("Solemnity of the Nativity")

    # Christmas Octave (25th December to 1st January)
    if ((tilburian_date.month == 12 and tilburian_date.day > 25) or 
        (tilburian_date.month == 1 and tilburian_date.day <= 1)):
        festival.append("Christmas Octave")

    # Easter Sunday
    for easter in easters_in_tilburian_year:
        if tilburian_date == easter:
            festival.append("Easter Sunday of the Resurrection of the Lord")

    # Easter Octave (Easter Sunday to the Sunday following Easter)
    for easter in easters_in_tilburian_year:
        if easter < tilburian_date <= easter + timedelta(days=7):
            festival.append("Easter Octave")
            break

    # Pentecost
    if tilburian_date in pentecost_dates:
        festival.append("Pentecost")
    
    # Feast of St. Januarius (September 19th) or Octave
    if tilburian_date.month == feast_of_st_januarius.month and tilburian_date.day == feast_of_st_januarius.day:
        festival.append("Feast of St. Januarius: Patron of Tilbury")
    elif feast_of_st_januarius.month == tilburian_date.month and feast_of_st_januarius.day < tilburian_date.day <= octave_of_gennaro_end.day:
        festival.append("Octave of St. Januarius")

    # Novena to St. Januarius - remembered by the broomsticks that brough Tilbury Her Patron
    if broomsticks_start <= tilburian_date <= broomsticks_end:
        festival.append("Novena to St. Januarius")

    # Kupus and Tilburian calendrical holidays
    if day == 1:
        festival.append("Festival of Kupus")
    if day == 380:
        festival.append("Festival of Kupus Eve")
    if day == 168:
        festival.append("Festival of Tilburian Vocations")
    if day == 82:
        festival.append("Moving Festival")
    if day == 125:
        festival.append("Festival of Le Capitaine")
    if day == 296:
        festival.append("Cleaning Day")

    festival_string = ", ".join(festival) if festival else ""

    # CALCULATING MONTHS

    # month for the current day
    month_name = day_to_month.get(day, "Unknown Month")

    # day of the month
    for month in custom_months:
        if month_name == month['month_name'] and month['start_day'] <= day <= month['end_day']:
            day_of_the_month = day - month['start_day'] + 1  # Day within the month (starting from 1)
            break
    else:
        day_of_the_month = "Unknown Day"

    dates.append([formatted_date, weekday_name, day, cycle_year_label, day_of_the_month, month_name, festival_string])

# save to .csv
filename = f"tilburian_year_{tilburian_year}.csv"
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Gregorian Date", "Weekday", "Tilburian Day (Year)", "Tilburian Cycle Year", "Tilburian Day (Month)", "Tilburian Month", "Festival"])
    writer.writerows(dates)

print(f"Tilburian calendar saved as {filename}")