
from src.models.shelter_sector_program import shelterSectorProgram


class youthShelter(shelterSectorProgram):
    def __init__(self, address, organizationName, name, city, postalCode, latitude,
                 longitude, sector, programName, data):
        # inheriting attributes from "shelter_sector_program" class
        super().__init__(address, organizationName, name, city, postalCode, latitude,
                         longitude, sector, programName, data)
        self.group = "Youth"
        # stores string representation of icon symbol that is displayed on map for objects in this class
        self.icon = "child"
        # stores string representation of color that is displayed on map for object
        self.iconColor = "orange"

    # inherits methods from parent class
    def addYouthToDefaultMap(self, map):
        return self.addMap( map)

    def get_youth_marker(self, map):
        return self.get_marker( map)

    def get_icon(self):
        return self.Icon()

    def sortedYouthOccupancies(self, getData):
        return self.quartileData(getData)

    def calculateFirstQuartileYouth(self):
        return self.calculateFirstQuartile()

    def calculateSecondQuartileYouth(self, getData):
        return self.calculateSecondQuartile()

    def calculateThirdQuartileYouth(self, getData):
        return self.calculateThirdQuartile()


