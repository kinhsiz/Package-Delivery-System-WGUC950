class CreatePackage:
    def __init__(self, package_id, address, city, zip_code, deadline, weight_kg, status, timestamp):
        self.id = package_id
        self.address = address
        self.city = city
        self.zipCode = zip_code
        self.deadlineTime = deadline
        self.weightKg = weight_kg
        self.status = status
        self.timestamp = timestamp

    def setStatus(self, new_status):
        # Method to set the status of the package
        self.status = new_status

    def getStatus(self):
        # Method to get the status of the package
        return self.status

    def setTimestamp(self, new_status):
        # Method to set the status of the package
        self.status = new_status

    def getTimestamp(self):
        # Method to get the status of the package
        return self.status

    # This will call the __str__ method to convert the object to a string and print it
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.city, self.zipCode,
                                                   self.deadlineTime, self.weightKg, self.status, self.timestamp)
