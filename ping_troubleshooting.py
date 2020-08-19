import ping3
import time
from csv import writer
import os
import datetime
import sys
import socket


def date_formatting():  # formats the date
    date_time = datetime.datetime.now()

    list_date_time.append(date_time)

    return date_time.strftime("%Y") + " " + date_time.strftime(
        "%B") + " " + date_time.strftime("%d") + " " + date_time.strftime("%X")


def ping_request():  # pings the two hostnames
    result_internet = ping3.ping(hostname_internet,
                                 unit='ms',
                                 timeout=timeout,
                                 ttl=64,
                                 size=32)
    result_router = ping3.ping(hostname_router,
                               unit='ms',
                               timeout=timeout,
                               ttl=64,
                               size=32)

    list_result_internet.append(result_internet)
    list_result_router.append(result_router)

    return result_internet, result_router


def legal_ip(ip):  # checks if it's a real IP address
    try:
        socket.inet_aton(ip)
        # print("legal IP address entered")
        exit_str = "1"
    except socket.error:
        print("Illegal IP address entered")
        exit_str = "0"
    return exit_str


def legal_float(number):  # checks if it's a real float
    try:
        number = float(number)
        # print("legal IP address entered")
        exit_str = "1"
    except ValueError:
        print("Illegal number entered")
        exit_str = "0"
    return exit_str, number


file_name = str(input("Enter filename:"))  # input file name

exit_str = "0"
while exit_str == "0":  # input polling rate with validity check
    polling_rate = input("Polling rate (default is 1.00s):")
    exit_str, polling_rate = legal_float(polling_rate)

exit_str = "0"
while exit_str == "0":  # input ping timeout with validity check
    timeout = input("Enter ping timeout (default is 0.45s):")
    exit_str, timeout = legal_float(timeout)

exit_str = "0"
while exit_str == "0":  # input first hostname with validity check
    hostname_internet = str(input("Enter external hostname (e.g. 8.8.8.8):"))
    exit_str = legal_ip(hostname_internet)

exit_str = "0"
while exit_str == "0":  # input second hostname with validity check
    hostname_router = str(input("Enter router hostname (e.g. 192.168.0.1):"))
    exit_str = legal_ip(hostname_internet)

if file_name[-4:] != ".csv":
    file_name = file_name + ".csv"

if os.path.isfile(file_name):  # delets file if user says so
    del_bool = input("Delete previous file (y/n)")
    if del_bool == "y" or del_bool == "Y":
        os.remove(file_name)
    else:
        print("Exiting program")
        sys.exit()
print("Creating new file called: " + file_name)

starttime = time.time()

list_date_time = []
list_result_internet = []
list_result_router = []

while True:  # loops forever
    date_time = date_formatting()
    result_internet, result_router = ping_request()

    with open(file_name, 'a+',
              newline='') as write_obj:  # appends data to file
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow([date_time, result_internet, result_router])

    print(date_time)
    try:  # print ping information about hostname
        print("ping to " + hostname_internet + " " *
              (20 - len(hostname_internet)) + format(result_internet, '.3f'))
    except TypeError:
        print("ping to " + hostname_internet + " " *
              (20 - len(hostname_internet)) + "lost")

    try:  # print ping information about router
        print("ping to " + hostname_router + " " *
              (20 - len(hostname_router)) + format(result_router, '.3f'))
    except TypeError:
        print("ping to " + hostname_router + " " *
              (20 - len(hostname_router)) + "lost")

    time.sleep(
        polling_rate -
        ((time.time() - starttime) % polling_rate))  # runs function every 1s
