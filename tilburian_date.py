import csv
from datetime import datetime
import sys
import subprocess
import time
import os

'''Runs Tilburian calendar to acquire needed calendar information.'''
def run_tilburian_calendar(date_str):
    try:
        subprocess.run(['python', 'tilburian_calendar.py', date_str], check=True)
        print("Tilburian calendar CSV generated successfully.")
    except subprocess.CalledProcessError:
        print("Error generating the Tilburian calendar CSV.")
        sys.exit(1)

'''Given the year, checks if the appropriately named calendar file exists. 
Waits to ensure generation in case run_tilburian_calendar was called.'''
def wait_for_csv_file(tilburian_year):
    file_path = f"tilburian_year_{tilburian_year}.csv"
    timeout = 10  # max wait time in seconds
    start_time = time.time()

    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            print(f"Error: CSV file {file_path} not found after waiting for {timeout} seconds.")
            sys.exit(1)
        time.sleep(1)

'''Given a Gregorian date, obtains and structures a Kupian/Tilburian date.'''
def get_tilburian_info_from_csv(gregorian_date):
    gregorian_date_str = gregorian_date.strftime("%A, %B %d, %Y")

    # calculate kupian year for .csv
    start_date = datetime(2009, 8, 23)
    tilburian_total_year = ((gregorian_date - start_date).days // 380) + 1

    # run a brief timer so .csv can be generated
    wait_for_csv_file(tilburian_total_year)
    
    # try to read the .csv and find the matching row
    try:
        with open(f"tilburian_year_{tilburian_total_year}.csv", mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['Gregorian Date'].strip() == gregorian_date_str:
                    tilburian_day = row['Tilburian Day (Month)']
                    tilburian_month = row['Tilburian Month']
                    tilburian_year = row['Tilburian Cycle Year']
                    festival = row['Festival'] if row['Festival'].strip() else 'none'
                    
                    return {
                        "Gregorian Date": gregorian_date_str,
                        "Tilburian Date": f"{tilburian_month} {tilburian_day},  {tilburian_year}",
                        "Festivals": festival
                    }
    except FileNotFoundError:
        return {"Error": "CSV file not found"}
    
    # if no match found in the CSV
    return {"Error": "No Tilburian information found for the given Gregorian date"}

# check if a date was provided as a command-line argument
if len(sys.argv) > 1:
    try:
        input_date = datetime.strptime(sys.argv[1], "%B %d, %Y")
    except ValueError:
        print("Invalid date format. Please use 'Month day, year' format (e.g., 'March 19, 2025').")
        sys.exit(1)
else:
    input_date = datetime.now()


# get the Tilburian information for the provided Gregorian date
run_tilburian_calendar(input_date.strftime("%B %d, %Y"))
tilburian_info = get_tilburian_info_from_csv(input_date)

# print the results
if "Error" not in tilburian_info:
    print(f"Gregorian Date: {tilburian_info['Gregorian Date']}")
    print(f"Tilburian Date: {tilburian_info['Tilburian Date']}")
    print(f"Festivals: {tilburian_info['Festivals']}")
else:
    print(tilburian_info["Error"])
