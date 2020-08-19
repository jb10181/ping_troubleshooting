import time
from csv import reader
import os
import datetime
import sys
from tkinter import filedialog
# import ipaddress
import matplotlib.pyplot as plt
import matplotlib.dates as dt


import_file_path = filedialog.askopenfilename()
print("Loading csv file: " + import_file_path)

list_date_time = []
list_result_internet = []
list_result_router = []

plt.ion()
fig, ax1 = plt.subplots()
plt.tight_layout()
ax1.plot(0, 0, color="r")
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot(0, 0, color="b")
ax2.set_yticks([], [])


with open(import_file_path) as csvDataFile:
    csvReader = reader(csvDataFile)
    # print(csvReader)
    for row in csvReader:
        list_date_time.append(row[0])
        list_result_internet.append(row[1])
        list_result_router.append(row[2])
        # print(row)

print(list_date_time)

while True:  # loops forever

    formatter = dt.DateFormatter("%Y-%m-%d-%X")
    ax1.xaxis.set_major_formatter(formatter)
    dates = list_date_time

    ax1.plot_date(dates,
                  list_result_internet,
                  linestyle="-",
                  color="b",
                  xdate=True,
                  ydate=False)
    ax1.plot_date(dates,
                  list_result_router,
                  linestyle="-",
                  color="r",
                  xdate=True,
                  ydate=False)

    ax1.set_ylabel('ping time (ms)', color="k")
    ax2.set_yticks([], [])
    ax1.legend([hostname_internet, hostname_router], loc='upper right')
    ax1.set_xlim([dates[0], dates[-1]])

    fig.canvas.draw()
    plt.pause(0.01)
    ax1.cla()
