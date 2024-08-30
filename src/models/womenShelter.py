
from src.models.shelter_sector_program import shelterSectorProgram


class womenShelter(shelterSectorProgram):
    def __init__(self, address, organizationName, name, city, postalCode, latitude, longitude, sector, programName, data):
        # inheriting attributes from shelter_sector_program
        super().__init__(address, organizationName, name, city, postalCode, latitude, longitude,sector, programName, data )
        self.group = "Women"
        # stores a string representation of the icon symbol displayed on map
        self.icon = "person-dress"
        # stores a string representation of the icon color display on map for objects in this class
        self.iconColor = "pink"

    # inheriting methods from parent class
    def addWomenToDefaultMap(self, map):
        return self.addMap( map)

    def get_women_marker(self, type_of_map):
        return self.get_marker( type_of_map)

    def sortedWomenData(self, getData):
        return self.quartileData(getData)


    def calculateFirstQuartileWomen(self):
        return self.calculateFirstQuartile()

    def calculateSecondQuartileWomen(self, getData):
        return self.calculateSecondQuartile()

    def calculateThirdQuartileWomen(self, getData):
        return self.calculateThirdQuartile()

    def get_icon(self):
        return self.Icon()
