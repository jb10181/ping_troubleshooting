from csv import reader
from tkinter import filedialog
import matplotlib.pyplot as plt
import sys
import tkinter
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

matplotlib.use("TkAgg")


def close_window(root):  # exits program
    print("Program exiting")
    root.destroy()
    sys.exit()


tkinter.Tk().withdraw()
import_file_path = filedialog.askopenfilename()  # loads csv
print("Loading csv file: " + import_file_path)

list_date_time = []  # imports csv data
list_result_internet = []
list_result_router = []
list_drops_internet_idx = []
list_drops_router_idx = []
with open(import_file_path) as csvDataFile:
    csvReader = reader(csvDataFile)
    count = 0
    for row in csvReader:
        if count == 0:
            hostname_internet = row[1]
            hostname_router = row[2]
        else:
            list_date_time.append(row[0])
            try:
                list_result_internet.append(float(row[1]))
            except ValueError:
                list_result_internet.append(None)
                list_drops_internet_idx.append(count)

            try:
                list_result_router.append(float(row[2]))
            except ValueError:
                list_result_router.append(None)
                list_drops_router_idx.append(count)
        count += 1
        # list_date_time.append(row[0])9

no_data = len(list_date_time)
no_drops_internet = len(list_drops_internet_idx)
no_drops_router = len(list_drops_router_idx)

per_drops_internet = round(100 * (no_drops_internet / no_data), 2)
per_drops_router = round(100 * (no_drops_router / no_data), 2)

list_drops_internet = [None] * no_data
for count in list_drops_internet_idx[::-1]:
    list_drops_internet[count - 1] = 0.

list_drops_router = [None] * no_data
for count in list_drops_router_idx[::-1]:
    list_drops_router[count - 1] = 0.

root = tkinter.Tk()  # gui root
root.title("Ping analysis tool")

figure = Figure(figsize=(10, 6), dpi=100)
plot = figure.add_subplot(1, 1, 1)

plot.plot_date(list_date_time,
               list_result_internet,
               linestyle="-",
               color="b",
               xdate=True,
               ydate=False)  # plots first hostname
plot.plot_date(list_date_time,
               list_result_router,
               linestyle="-",
               color="r",
               xdate=True,
               ydate=False)  # plots second hostname

plot.plot_date(list_date_time,
               list_drops_internet,
               linestyle="-",
               color="k",
               xdate=True,
               ydate=False)  # plots first hostname drops
plot.plot_date(list_date_time,
               list_drops_router,
               linestyle="-",
               color="y",
               xdate=True,
               ydate=False)  # plots second hostname drops

no_ticks = 4  # sets number of x axis labels
plot.xaxis.set_major_locator(plt.MaxNLocator(no_ticks))

plot.set_ylabel('ping time (ms)', color="k")  # sets graph parameters
plot.legend([
    hostname_internet + " Packets received " + str(100 - per_drops_internet) +
    "%", hostname_router + " Packets received " + str(100 - per_drops_router) +
    "%", hostname_internet + " Packets dropped " + str(per_drops_internet) +
    "%", hostname_router + " Packets dropped " + str(per_drops_router) + "%"
],
            loc='upper right')
plot.set_xlim([list_date_time[0], list_date_time[-1]])

canvas = FigureCanvasTkAgg(figure, root)  # plot graph
canvas.get_tk_widget().grid(row=1, column=0, sticky='nesw')

toolbarFrame = tkinter.Frame(master=root)  # navigation toolbar
toolbarFrame.grid(row=2, column=0)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

label1 = tkinter.Label(root, text="Command", font="bold")  # command title
label1.grid(row=0, column=1)

label2 = tkinter.Label(root, text="Keyboard Shortcut(s)",
                       font="bold")  # shortcut title
label2.grid(row=0, column=2)

# command list
comm_str3 = "Home/Reset \n Pan/Zoom \n Zoom-to-rect \n Save \n Constrain pan/zoom to x axis \n Constrain pan/zoom to y axis"
label3 = tkinter.Label(root, text=comm_str3)
label3.grid(row=1, column=1, sticky="n")
# shortcut list
comm_str4 = "h or r or home \n p \n o \n ctrl + s \n hold x when panning/zooming with mouse \n hold y when panning/zooming with mouse"
label4 = tkinter.Label(root, text=comm_str4)
label4.grid(row=1, column=2, sticky="n")

button = tkinter.Button(root,
                        text="Exit program",
                        command=lambda: close_window(root))  # exit button
button.grid(row=0, column=0, sticky="ne")

root.mainloop()
