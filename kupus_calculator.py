from datetime import datetime, timedelta

# establish Kupus start date and interval of 380 day Tilburian Calendar
start_date = datetime(2009, 8, 23)
interval = timedelta(days = 380)
current_date = start_date
i = 0  # cycle counter

# while Kupus date is not past current year, calculate date and cycle
while current_date.year <= datetime.now().year:
    cycle_year = (i % 10) + 1  # cycle resets every 10 years
    year_of_the = "Watermelon" if cycle_year == 10 else "Cabbage"
    formatted_date = current_date.strftime("%A, %B %d, %Y")
    
    print(f"{formatted_date} - {year_of_the}")
    current_date += interval
    i += 1
