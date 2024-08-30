
from src.models.shelter_sector_program import shelterSectorProgram


class CoedShelter(shelterSectorProgram):
    def __init__(self, address, organizationName, name, city, postalCode, latitude,
                 longitude, sector, programName, data):
        # inheriting attributes from "shelter_sector_program"
        super().__init__(address, organizationName, name, city, postalCode, latitude,
                         longitude, sector,programName, data )
        # filling in attributes with values relevant to this class
        self.group = "Co-ed"
        # stores string name of icon symbol that will be displayed on map
        self.icon= "children"
        # stores string representation of icon color that will be display on map
        self.iconColor = "purple"

    # inheriting parent methods
    def addCoedToDefaultMap(self, map):
        return self.addMap( map)

    def get_coed_marker(self, type_of_map):
        return self.get_marker( type_of_map)

    def sortedOccupancyCoData(self, getData):
        return self.quartileData(getData)

    def calculateFirstQuartileCo(self):
        return self.calculateFirstQuartile()

    def calculateSecondQuartileCo(self):
        return self.calculateSecondQuartile()

    def calculateThirdQuartileCo(self):
        return self.calculateThirdQuartile()

    def createcoicon(self):
        return self.Icon()
