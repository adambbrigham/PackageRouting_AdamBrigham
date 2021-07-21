


import csv
import sys

import Package
import hashTable

import Truck

package_list = []
ids_list = []


# read package information from csv and create package objects with fields from file
def parse_package(filename):
    with open(filename) as packages:
        package_data = csv.reader(packages, delimiter=',')
        for package in package_data:
            ID = int(package[0])
            address = package[1]
            city = package[2]
            zip = package[4]
            deadline = package[5]
            weight = package[6]
            package = Package.Package(ID, address, city, zip, deadline, weight)
            myHash.insert(ID, package)
            package_list.append(address)
            ids_list.append(ID)


# read distances from csv file and create a 2d array to hold indexed data
with open('DistanceList.csv') as csvDataFile:
    # csvDistance = csv.reader(csvDataFile)
    distances = [row for row in csv.reader(csvDataFile)]

# read addresses from csv file and add them to list
addresses = []
with open('AddressList.csv') as csvDataFile:
    # csvDistance = csv.reader(csvDataFile)
    address_data = csv.reader(csvDataFile, delimiter=',')
    for data in address_data:
        addresses.append(data[0].strip())


# Gets the distance between two addresses
def distance_between(address1, address2):
    # gets string data from Distances 2D array
    dist = distances[addresses.index(address1)][addresses.index(address2)]
    # if string is empty switch parameter order and cast to float
    if dist == "":
        dist = float(distances[addresses.index(address2)][addresses.index(address1)])
    # else maintain parameter order and cast to float
    else:
        dist = float(distances[addresses.index(address1)][addresses.index(address2)])
    return dist


# counts the number of rows in spreadsheet csv files
def count_rows(filename):
    with open(filename) as rows:
        counter = 0
        spreadsheet = csv.reader(rows, delimiter=',')
        for row in spreadsheet:
            counter = counter + 1
    return counter


# create hashtable with package objects
num_packages = count_rows('PackageList.csv')
myHash = hashTable.HashTable(num_packages)
parse_package('PackageList.csv')


# algorithm to determine delivery order of packages based on distance between addresses
# "Nearest Neighbor" based
def algo_order_package_ids(ids_list_parameter):
    min_index = -1
    # empty ids list
    algo_ids = []
    # start at hub
    current_address = "HUB"
    # fill list until it contains all ids
    while len(algo_ids) < len(ids_list_parameter):
        # initiate with value higher than in distance list
        min_distance = 1000.0
        for i in range(len(ids_list_parameter)):
            # check to get the minimum distance between addresses
            # checks that id is not in the ids list, otherwise the nearest address is the previous address
            if distance_between(myHash.lookup(ids_list_parameter[i]).address.strip(), current_address) < min_distance \
                    and ids_list_parameter[i] not in algo_ids:
                # set min distance using hashtable lookup
                min_distance = distance_between(myHash.lookup(ids_list_parameter[i]).address.strip(), current_address)
                # set index of current min distance in loop
                min_index = i
        # set current address after completion of inner loop
        current_address = myHash.lookup(ids_list_parameter[min_index]).address.strip()
        # add id to list in order
        algo_ids.append(ids_list_parameter[min_index])
    return algo_ids


# load trucks with package ids
# driver 1, leaves 8.00
packages_for_truck1 = [6, 14, 13, 15, 16, 20, 30, 31, 29, 34]
# driver 1, leaves when truck 1 returns
packages_for_truck2 = [2, 3, 9, 18, 19, 21, 22, 23, 24, 26, 27, 33, 35, 36, 38, 39]
# driver 2, leaves 9.05
packages_for_truck3 = [1, 4, 5, 7, 8, 10, 11, 12, 17, 25, 28, 32, 37, 40]

# create truck objects and pass ordered package ids to constructor
truck1 = Truck.Truck(algo_order_package_ids(packages_for_truck1))
truck2 = Truck.Truck(algo_order_package_ids(packages_for_truck2))
truck3 = Truck.Truck(algo_order_package_ids(packages_for_truck3))


# calculate pseudo-time based on rate and distance travelled by trucks
def calculate_time(distance):
    # t = d/r
    return distance / 18.00


# algorithm to deliver packages using truck objects
def begin_deliveries(truck, start_time):
    current_time = 0.0
    current_address = "HUB"
    distance = 0
    # loops through ordered package ids on truck
    for i in truck.package_list:
        # sets timestamp leaving the hub to start_time parameter
        myHash.lookup(i).timestamp_leaving_hub = start_time
        # distance accumulates with each delivery
        distance = distance + distance_between(myHash.lookup(i).address, current_address)
        # time accumulates with each delivery
        current_time = start_time + calculate_time(distance)
        # set delivery time and change package status
        myHash.lookup(i).timestamp_delivered = current_time
        myHash.lookup(i).status = "Delivered"
        # set current address to be compared to in next iteration
        current_address = myHash.lookup(i).address
    # return to hub and add distance and time to truck fields
    truck.distance = distance + distance_between(current_address, "HUB")
    truck.time = current_time + calculate_time(distance)


# begin truck deliveries
begin_deliveries(truck1, 8.00)
begin_deliveries(truck2, 10.90)
begin_deliveries(truck3, 9.10)


# menu and command line user interface
def menu():
    user_input = ""
    # print menu until user quits
    while user_input != "q":
        # format menu for user interface
        print("\n************************* MENU *************************")
        print("| \"a\" --    display all packages at end of day         |")
        print("| \"b\" -- display all packages at a specific time       |")
        print("| \"c\" -- display a specific package at a specific time |")
        print("| \"d\" --    display total mileage at end of day        |")
        print("********************************************************")
        user_input = input("\n\t\tSelect from the menu options (\"q\" to quit)")  # get user input
        # if-else logic to handle user input
        if user_input == "q":
            # quit
            sys.exit()
        elif user_input == "a":
            # print all package info at end of day
            user_print_all()
        elif user_input == "b":
            # all packages at specific time
            user_print_all_at_time(float(input("Enter an inquiry time (decimal format e.g: 9.75):")))
        elif user_input == "c":
            # specific package at specific time
            user_package = int(input("Enter a package ID:"))
            user_time = float(input("Enter an inquiry time (decimal format e.g: 9.75):"))
            user_print_single_at_time(user_package, user_time)
        elif user_input == "d":
            # show mileage summary
            display_mileage()
        else:
            # handle invalid user inputs
            print("Please enter a valid input:")


# prints all packages at end of day
def user_print_all():
    # loop through packages in numerical ID order
    for i in range(len(myHash.table)):
        # time to ##:## format
        time = myHash.lookup(i + 1).timestamp_delivered
        hours = int(time)
        minutes = int((time * 60) % 60)
        print(myHash.lookup(i + 1))
        # if not delivered, then set time to N/A
        if myHash.lookup(i + 1).status != "Delivered":
            time = "N/A"
            print("\t\t| Delivery Time: {:>24}".format(time))
        else:
            print("\t\t| Delivery Time: {:>21}:{:0>2}".format(hours, minutes))


# prints all packages at a specific time
def user_print_all_at_time(inquiry_time):
    for i in range(len(myHash.table)):
        time = myHash.lookup(i + 1).timestamp_delivered
        hours = int(time)
        minutes = round(time * 60 % 60)

        # handle the incorrect address
        if myHash.lookup(i + 1).ID == 9 and inquiry_time < 10.33:
            myHash.lookup(i + 1).address = "300 State St"
            myHash.lookup(i + 1).zip = "84103"

        # if not delivered, set status according to timestamps and inquiry time
        if myHash.lookup(i + 1).timestamp_leaving_hub < inquiry_time <= myHash.lookup(i + 1).timestamp_delivered:
            myHash.lookup(i + 1).status = "En Route"
        elif myHash.lookup(i + 1).timestamp_leaving_hub >= inquiry_time:
            myHash.lookup(i + 1).status = "At the hub"

        # prints package information
        # if not delivered, then set time to N/A
        print(myHash.lookup(i + 1))
        if myHash.lookup(i + 1).status != "Delivered":
            time = "N/A"
            print("\t\t| Delivery Time: {:>24}".format(time))
        else:
            print("\t\t| Delivery Time: {:>21}:{}".format(hours, minutes))


# prints a single package at a specific time
def user_print_single_at_time(user_package, user_time):
    time = myHash.lookup(user_package).timestamp_delivered
    hours = int(time)
    minutes = round(time * 60 % 60)

    # handle the incorrect address
    if myHash.lookup(user_package).ID == 9 and user_time < 10.33:
        myHash.lookup(user_package).address = "300 State St"
        myHash.lookup(user_package).zip = "84103"

    # if not delivered, set status according to timestamps and inquiry time
    if myHash.lookup(user_package).timestamp_leaving_hub < user_time <= myHash.lookup(user_package).timestamp_delivered:
        myHash.lookup(user_package).status = "En Route"
    elif myHash.lookup(user_package).timestamp_leaving_hub >= user_time:
        myHash.lookup(user_package).status = "At the hub"

    # prints package information
    # if not delivered, then set time to N/A
    print(myHash.lookup(user_package))
    if myHash.lookup(user_package).status != "Delivered":
        time = "N/A"
        print("\t\t| Delivery Time: {:>24}".format(time))
    else:
        print("\t\t| Delivery Time: {:>21}:{}".format(hours, minutes))


# display mileage summary
def display_mileage():
    total_distance_all_trucks = truck1.distance + truck2.distance + truck3.distance
    print("\n****** Distances ******")
    print("| Truck 1: {0:.1f} miles |".format(truck1.distance))
    print("| Truck 2: {0:.1f} miles |".format(truck2.distance))
    print("| Truck 3: {0:.1f} miles |".format(truck3.distance))
    print("_______________________")
    print("| Total:   {0:.1f} miles |".format(total_distance_all_trucks))


# run menu method
menu()

