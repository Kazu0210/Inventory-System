import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Example data (replace with your actual data)
dates = ['2024-11-01', '2024-11-02', '2024-11-03', '2024-11-04', '2024-11-05']
orders = [12, 15, 10, 25, 18]

# Convert string dates to datetime objects
dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

# Create the line plot
plt.figure(figsize=(10, 6))
plt.plot(dates, orders, marker='o', linestyle='-', color='b')

# Format the x-axis with date labels
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

# Rotate the date labels to fit them nicely
plt.xticks(rotation=45)

# Adding titles and labels
plt.title('Daily Orders', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Orders', fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()
