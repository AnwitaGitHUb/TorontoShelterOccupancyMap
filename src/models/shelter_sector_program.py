import folium as fl
import numpy as np
from src import constants as c
from src.models import shelter_program as spc


# creating a class to store sector information and methods
class shelterSectorProgram(spc.shelterProgram):

    def __init__(self, address, organizationName, name, city, postalCode, latitude,
                 longitude, sector, programName, data):
        # inheriting attributes from program class
        super().__init__(address, organizationName, name, city, postalCode, latitude,
                         longitude, programName, data)
        # initializing abstract attributes to use in functions
        # subclasses can  rename these attributes to match their purpose and then use methods of this class without
        # inputting new parameters
        # sectors include Women, Men, Youth, Co-ed
        self._sector = sector
        self.group = ""
        self.icon = ""
        self.iconColor = ""

    # create marker that is added to map layer that includes all shelter sectors
    def addMap(self, type_of_map):
        if self.getSector() == self.group:
            fl.Marker(
                location=(self.getLatitude(), self.getLongitude()),
                axis=1,
                popup=self.popUpText(),
                # set icon color to color attribute of class, set icon to symbol attribute of class
                icon=fl.Icon(prefix="fa", color=self.iconColor, icon=self.icon)).add_to(type_of_map)

    # creating marker that is added to map layer that just includes all programs with sector of the object
    def get_marker(self, type_of_map):
        if self.getSector() == self.group:
            fl.Marker(
                location=(self.getLatitude(), self.getLongitude()),
                axis=1,
                popup=self.popUpText(),
                icon=self.Icon()
            ).add_to(type_of_map)

    # creating a sorted list of average occupancies for programs with the same sector as object
    def quartileData(self, data):
        # creating a new dataframe by filtering original dataframe to just include rows with object's sector
        quartile = data[data[c.DATA_SECTOR] == self.group]
        average_occupancies = []

        for index, row in quartile.iterrows():
            if len(row[c.DATA_OCCUPANCIES]) != 0:
                # calculate average occupancy of a program and add to a list
                average_occupancies.append(sum(row[c.DATA_OCCUPANCIES]) // len(row[c.DATA_OCCUPANCIES]))
        average_occupancies.sort()
        return average_occupancies
    # calculating different quartiles of sorted list
    def calculateFirstQuartile(self):
        """

        :return: a float which represents the firstQuartile of the sorted average occupancies list
        """
        if self._sector == self.group:
            firstQuartile = np.quantile(self.quartileData(self.getData()), 0.25)
            return firstQuartile

    def calculateSecondQuartile(self):
        """

        :return: a float which represents the secondQuartile of the sorted average occupancies list
        """
        if self._sector == self.group:
            secondQuartile = np.quantile(self.quartileData(self.getData()), 0.50)
            return secondQuartile

    def calculateThirdQuartile(self):

        """

        :return: a float which represents the thirdQuartile of the sorted average occupancies list
        """
        if self._sector == self.group:
            thirdQuartile = np.quantile(self.quartileData(self.getData()), 0.75)
            return thirdQuartile

    def Icon(self):
        """

        :return: folium icon that is displayed on the map
        """
        if self.getSector() == self.group:

            # if average occupancy is between/ equal to 3rd and 4th quartile, make icon red
            if self.calculateAverageDailyOccupancy() >= self.calculateThirdQuartile( ):

                icon = fl.Icon(prefix="fa", color="red", icon=self.icon)
                return icon
            # if avg occupancy is between or equal to 2nd and 3rd quartile, make icon orange
            elif self.calculateAverageDailyOccupancy() >= self.calculateSecondQuartile(
            ) and self.calculateAverageDailyOccupancy(
            ) < self.calculateThirdQuartile():
                icon = fl.Icon(prefix="fa", color="orange", icon=self.icon)
                return icon
            # if avg occupancy is between or equal to 1st and 2nd quartile, make icon beige
            elif self.calculateAverageDailyOccupancy() >= self.calculateFirstQuartile(
            ) and self.calculateAverageDailyOccupancy(
            ) < self.calculateSecondQuartile():
                icon = fl.Icon(prefix="fa", color="beige", icon=self.icon)
                return icon
            # if avg occ is below 1st quartile, make icon green
            else:
                icon = fl.Icon(prefix="fa", color="green", icon=self.icon)
                return icon

    def getSector(self):
        return self._sector
