import csv
import hashTable
# class for package objects
class Package:
    # constructor for package objects
    def __init__(self, ID, address, city, zip, deadline, weight):
        self.ID = ID
        self._address = address
        self._deadline = deadline
        self._city = city
        self._zip = zip
        self._weight = weight
        # default values for status and timestamps fields
        self._status = "At the hub"
        self._timestamp_leaving_hub = 0.0
        self._timestamp_delivered = 0.0

    # to_string method formatted for reports to user
    def __str__(self):
        return "\t\t_________________________________________\n" \
               "ID: {:0>2}  | Address: {:>30} \n\t\t| City: {:>33} \n\t\t| Zip: {:>34} \n\t\t| Deadline: {:>29} \n\t\t|" \
               " Weight: {:>31} \n\t\t| Status: {:>31}" \
               .format(self.ID, self.address, self.city, self.zip, self.deadline, self.weight, self.status)


    #setters and getters for package fields
    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        self._deadline = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value

    @property
    def zip(self):
        return self._zip

    @zip.setter
    def zip(self, value):
        self._zip = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def timestamp_leaving_hub(self):
        return self._timestamp_leaving_hub

    @timestamp_leaving_hub.setter
    def timestamp_leaving_hub(self, value):
        self._timestamp_leaving_hub = value

    @property
    def timestamp_delivered(self):
        return self._timestamp_delivered

    @timestamp_delivered.setter
    def timestamp_delivered(self, value):
        self._timestamp_delivered = value

