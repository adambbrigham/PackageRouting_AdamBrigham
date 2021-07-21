# class for truck objects to carry and deliver the packages
# and record the distance travelled as a field
class Truck:
    # constructor for truck objects
    def __init__(self, package_list):
        self.package_list = package_list
        self.distance = 0.0
        self.time = 0.0
        self.rate = 18.0

    # setters and getters for truck fields
    @property
    def package_list(self):
        return self._package_list

    @package_list.setter
    def package_list(self,value):
        self._package_list = value

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self,value):
        self._distance = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self,value):
        self._rate = value








