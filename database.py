import IP2Location


# Taylor Shoultz, Grant Bourque

class Database:
    """Class for getting location data from the IP2Location database"""

    def __init__(self):
        """Creates an object with IP2Location API"""
        self.database = IP2Location.IP2Location("IP2LOCATION-LITE-DB11.BIN")

    def get_location(self, ip):
        """Return a list that has Latitude = 0, Longitude = 1, Country = 2, Region = 3"""
        sender = self.database.get_all(ip)
        return [sender.latitude, sender.longitude, sender.country_long, sender.region]
