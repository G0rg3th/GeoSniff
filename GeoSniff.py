#This is the main script to run the project GeoSniff

import IP2Location

#Class for getting data from the database
class Database:

    # Creates a object with IP2Location API
    def __init__(self):
        self.database = IP2Location.IP2Location("IP2LOCATION-LITE-DB11.BIN")

    #Return a list thet has Latitude = 0, Longitude = 1, Country = 2, city = 3
    def getLocation(self, ip):
        sender = self.database.get_all(ip)
        ret = [sender.latitude, sender.longitude, sender.country_long, sender.city]
        return ret

data = Database()
loc = data.getLocation("114.160.112.27")
print loc[2]
