from csv import reader
from tkinter import filedialog
import matplotlib.pyplot as plt
# import matplotlib.dates as dt
import tkinter
from tkinter.ttk import *
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import_file_path = filedialog.askopenfilename()
print("Loading csv file: " + import_file_path)

list_date_time = []
list_result_internet = []
list_result_router = []
with open(import_file_path) as csvDataFile:
    csvReader = reader(csvDataFile)
    # print(csvReader)
    count = 0
    for row in csvReader:
        if count == 0:
            hostname_internet = row[1]
            hostname_router = row[2]
        else:
            list_date_time.append(row[0])
            list_result_internet.append(float(row[1]))
            list_result_router.append(float(row[2]))
        # print(row)
        count += 1

root = tkinter.Tk()

figure = Figure(figsize=(10, 6), dpi=100)
plot = figure.add_subplot(1, 1, 1)

dates = list_date_time

# formatter = dt.DateFormatter("%Y-%m-%d-%X")
# plot.xaxis.set_major_formatter(formatter)
# dates = list_date_time

plot.plot_date(dates,
               list_result_internet,
               linestyle="-",
               color="b",
               xdate=True,
               ydate=False)
plot.plot_date(dates,
               list_result_router,
               linestyle="-",
               color="r",
               xdate=True,
               ydate=False)

no_ticks = 4
plot.xaxis.set_major_locator(plt.MaxNLocator(no_ticks))

plot.set_ylabel('ping time (ms)', color="k")
plot.legend([hostname_internet, hostname_router], loc='upper right')
plot.set_xlim([dates[0], dates[-1]])

canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().grid(row=0, column=0, sticky='nw')

scrollbar = tkinter.Scrollbar(root,
                              orient="horizontal")
scrollbar['command'] = canvas.get_tk_widget().xview
scrollbar.grid(row=1, column=0, sticky='nsew')
# canvas.configure(xscrollcommand=scrollbar.set)

# canvas.config(scrollregion=canvas.bbox("all"))

# scrollbar["command"] = canvas.get_tk_widget().xview
# canvas.get_tk_widget()["xscrollcommand"] = scrollbar.set

# scrollbar = tkinter.Scrollbar(master=root)
# scrollbar.pack(side=tkinter.BOTTOM)
# scrollbar["command"] = canvas.get_tk_widget().xview
# canvas.get_tk_widget()["xscrollcommand"] = scrollbar.set
# scrollbar = tkinter.Scrollbar(root, orient="horizontal")
# scrollbar.grid(row=1, column=0, sticky='s')
# # scrollbar["command"] = canvas.get_tk_widget().xview
# # canvas.get_tk_widget()["xscrollcommand"] = scrollbar.set
#
# scrollbar["command"] = canvas.get_tk_widget().xview
# canvas.get_tk_widget()["xscrollcommand"] = scrollbar.set
root.mainloop()
