from datetime import datetime

date_time = "2023-07-25 14:30:00"
dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
time = dt.strftime("%H:%M:%S")

time_12hr = dt.strftime("%Y-%m-%d %I:%M:%S %p")

print(time_12hr)