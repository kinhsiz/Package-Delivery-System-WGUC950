import csv
import datetime

import truck
from Package import CreatePackage
from createHashTable import CreateHashTable


# STUDENT ID: 009971354

#  Function to load data from csv package file.
def loadPackageData(file):
    with open(file) as packages:
        packageData = csv.reader(packages, delimiter=',')

        for elem in packageData:
            packageid = int(elem[0])
            address = elem[1]
            city = elem[2]
            zipcode = elem[4]
            deadline = elem[5]
            weight = elem[6]
            status = "at hub"
            timestamp = "00:00"

            package = CreatePackage(packageid, address, city, zipcode, deadline, weight, status, timestamp)
            packageHashTable.insert(packageid, package)


packageHashTable = CreateHashTable()
loadPackageData('packageFile.csv')


# ------------------------DISTANCE-----------------------------------
# Function to load data from distance csv file

def loadDistanceData(file):
    with open(file) as distance:
        distanceData = list(csv.reader(distance, delimiter=','))
    return distanceData


# assigns file data to variable
distanceTable = loadDistanceData('distanceFile.csv')

# -----------------------ADDRESSES ------------------------------------


# Function to load csv address file.
def loadAddressData(file):
    with open(file) as address:  # with open, funct closes the file w/o using close()
        addressData = csv.reader(address, delimiter=',')
        addressDic = dict(addressData)
        return addressDic


# Assigns file data  to variable
addressTable = loadAddressData('addressFile.csv')


# ----------------Loading Packages------------------------------
# Function that return distance between two addresses.
def findDistance(pointA, pointB):
    pointAInt = int(addressTable[pointA])
    pointBInt = int(addressTable[pointB])
    distance = distanceTable[pointAInt][pointBInt]

    if distance == '':
        distance = distanceTable[pointBInt][pointAInt]
        return float(distance)
    else:
        return float(distance)


# Create three Truck objects to manually load trucks
nina1 = truck.CreateTruck(1, 25, 13, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
                          '4001 South 700 East', datetime.timedelta(hours=8), datetime.timedelta(hours=8), 0.00)

pinta2 = truck.CreateTruck(2, 47, 10, [3, 6, 18, 25, 26, 27, 28, 32, 36, 38, 39],
                           '4001 South 700 East', datetime.timedelta(hours=9, minutes=20),
                           datetime.timedelta(hours=9, minutes=20), 0.00)

santaMaria3 = truck.CreateTruck(3, 0, 16, [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 33, 35],
                                '4001 South 700 East', datetime.timedelta(hours=11), datetime.timedelta(hours=11), 0.00)


# Function that delivers packages by finding the next shortest distance from last location.
def nearestNeighbor(truckName, hashTable, user_time, userInput):
    currentPoint = '4001 South 700 East'  # Initial location at the hub
    undelivered = []  # total number of packages in a truck  # for elem in packageList: print(elem)

    # Look up for packages in hash table and if found, append to undelivered variable
    for packId in truckName.packageList:
        package = hashTable.lookup(packId)
        undelivered.append(package)
    truckName.packageList.clear()

    # Function that returns the next shortest distance from a list
    def returnMin(packs, currentLoc):
        minDistance = float('inf')
        nextNeighbor = None
        for point in packs:
            distance = findDistance(currentLoc, point.address)
            if distance < minDistance:
                minDistance = distance
                nextNeighbor = point
        return nextNeighbor, minDistance

    # Loop will continue iterating until all packages are delivered
    while undelivered:
        nearNeighbor, newDistance = returnMin(undelivered, currentPoint)
        truckName.packageList.append(nearNeighbor)
        currentPoint = nearNeighbor.address  # Assigns last location
        packageStatus = hashTable.lookup(nearNeighbor.id)

        # Obtains package delivery time
        truckName.departTime += datetime.timedelta(hours=newDistance / 18)
        print(truckName.departTime)

        undelivered.remove(nearNeighbor)
        truckName.currentMileage += newDistance
        packageStatus.timestamp = truckName.departTime

        # Changes package address to a different address after 10:20 am
        if nearNeighbor.id == 9 and user_time >= datetime.timedelta(hours=10, minutes=20):
            packageStatus.address = "410 S State St,Salt Lake City,UT,84111,EOD,5,"
        # If-statement to update package current status depending on user time
        if user_time <= truckName.loading:
            packageStatus.status = "at hub"
            packageStatus.timestamp = "00:00"
        elif user_time < packageStatus.timestamp:
            packageStatus.status = "in route"
            packageStatus.timestamp = "00:00"
        elif user_time >= packageStatus.timestamp:
            packageStatus.status = "delivered"

    # Prints all packages
    if truckName == santaMaria3 and userInput == "1":
        for i in range(len(packageHashTable.table)):
            print('Package: ', packageHashTable.lookup(i + 1))

    return packageHashTable

    #  print(float("{:.2f}".format(truckName.currentMileage)))


# --------------------------User Interface----------------------------------

print("Welcome to Western Governors University Parcel Service")


# This code is the user interface to request info of a package
def userInterface():
    print()
    print("What time would you like to see the package delivery status of?")
    userTime = input("Please, enter our input in format HH:MM: ")

    try:
        # Parses the user input as a time in 'HH:MM' format
        hours, minutes = map(int, userTime.split(':'))
        # Attempt to parse user input as a datetime object
        userDatetime = datetime.timedelta(hours=hours, minutes=minutes)
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            print()
            print("Pick an option:")
            print()
            print("Type 1 if you want to see the delivery status of all packages")
            print("Type 2 if you want to see the delivery status on a single package")
            print("Type 3 to exit")
            user_inputA = input("Your input: ")
            # Exit the loop if the user enters '3'
            if user_inputA == "3":
                exit()
            # Prints delivery status of all packages
            if user_inputA == "1":
                nearestNeighbor(nina1, packageHashTable, userDatetime, user_inputA)
                nearestNeighbor(pinta2, packageHashTable, userDatetime, user_inputA)
                nearestNeighbor(santaMaria3, packageHashTable, userDatetime, user_inputA)
                totalMileage = pinta2.currentMileage + nina1.currentMileage + santaMaria3.currentMileage
                print()
                print("Total mileage for all routes is:", "", totalMileage, "miles.")

            # Prints only a particular  package requested by user
            if user_inputA == "2":
                nearestNeighbor(nina1, packageHashTable, userDatetime, user_inputA)
                nearestNeighbor(pinta2, packageHashTable, userDatetime, user_inputA)
                nearestNeighbor(santaMaria3, packageHashTable, userDatetime, user_inputA)
                totalMileage = pinta2.currentMileage + nina1.currentMileage + santaMaria3.currentMileage
                print()
                print("Total mileage for all routes is:", "", totalMileage, "miles.")
                print("Please, enter a package ID:")
                user_inputB = input("Your input:  ")
                print(packageHashTable.lookup(int(user_inputB)))
        else:
            print("Invalid time format. Hours should be between 0 and 23, and minutes should be between 0 and 59.")
    except ValueError:
        print("Invalid time format. Please enter time in 'HH:MM' format.")


userInterface()
