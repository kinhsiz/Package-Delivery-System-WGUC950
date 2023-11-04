class CreateTruck:
    def __init__(self, truckID, driverID, totalPackages, packageList, location, loadingTime, departTime, currentMileage):
        self.truckID = truckID
        self.driverID = driverID
        self.packages = totalPackages
        self.loading = loadingTime
        self.packageList = packageList
        self.location = location

        self.departTime = departTime
        self.currentMileage = currentMileage

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s,%s,%s" % (self.truckID, self.driverID, self.packages, self.packageList, self.location,
                                            self.loading, self.departTime, self.currentMileage)
