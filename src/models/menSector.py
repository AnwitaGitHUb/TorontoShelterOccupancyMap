
from src.models.shelter_sector_program import shelterSectorProgram


class ProgramMen(shelterSectorProgram):
    def __init__(self, address, organizationName, name, city, postalCode, latitude, longitude, sector, programName, data):
        # inheriting attributes from "shelter_sector_program"
        super().__init__(address, organizationName, name, city, postalCode, latitude, longitude, sector, programName, data)
        # filling in attributes with values relevant to this class
        self.group = "Men"
        # stores string name of icon symbol that will be displayed on map
        self.icon = "person"
        # stores string representation of icon color that will be display on map
        self.iconColor = "blue"

    # inheriting parent methods
    def addMenToDefaultMap(self, map):
        return self.addMap( map)

    def get_men_marker(self, type_of_map):
        return self.get_marker( type_of_map)

    def get_icon(self):
        return self.Icon()

    def quartileMenData(self, getData):
        return self.quartileData(getData)

    def calculateFirstQuartileMen(self):
        return self.calculateFirstQuartile()

    def calculateSecondQuartileMen(self, getData):
        return self.calculateSecondQuartile()

    def calculateThirdQuartileMen(self, getData):
        return self.calculateThirdQuartile()
