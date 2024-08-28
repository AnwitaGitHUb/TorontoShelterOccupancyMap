import numpy
import pandas as pd
from src import constants as c
from src.models import shelter as sc


class shelterProgram(sc.Shelter):
    def getData(self):
        return self._data

    # initializing constructor
    def __init__(self, address, organizationName, name, city, postalCode, latitude, longitude,
                 program, data):
        # inheriting all attributes from parent class
        super().__init__(address, organizationName, name, city, postalCode, latitude, longitude, data)
        self._program = program

    def calculateAverageDailyOccupancy(self):
        for index, row in self.getData().iterrows():
            if row[c.DATA_PROGRAM_NAME] == self._program:
                # taking sum of all occupancies throughout the year and dividing by number of days to get average
                dailyAverageOccupancy = sum(row[c.DATA_OCCUPANCIES]) // len(row[c.DATA_OCCUPANCIES])
                return dailyAverageOccupancy

    def calculateAverageDailyOccupancyRate(self):
        # variable to store ongoing averages
        occ_rate_sum = 0
        count = 0  # To count valid occupancy rates
        for index, row in self.getData().iterrows():
            if row[c.DATA_PROGRAM_NAME] == self._program:
                for idx, occupancy in enumerate(row[c.DATA_OCCUPANCIES]):
                    # preventing division by 0 errors
                    if row[c.DATA_CAPACITIES][idx] != 0:
                        # for every day of the program's operation, each occupancy is divided by capacity for the day
                        occ_rate_sum += occupancy / row[c.DATA_CAPACITIES][idx]
                        count += 1
        if count == 0:
            return  # To avoid division by zero if there are no valid entries
        average_rate_sum = (occ_rate_sum / count) * 100
        return average_rate_sum

    def popUpText(self):
        # generating text that will be displayed on popup with shelter's information including program
        popUpText = (f"popup'> Organization Name: {self.getOrganizationName()}, Shelter Address: {self.getAddress()}, "
                     f"Name of Shelter: {self.getShelterName()}, Name of Program: {self.getProgramName()} City: {self.getCity()}, Postal Code: {self.getPostalCode()}, "
                     f" Average Annual Occupancy:{self.calculateAverageDailyOccupancy()}, Average Annual Rate of Occupancy:"
                     f"{self.calculateAverageDailyOccupancyRate()}% </div>")
        return popUpText

    def getProgramName(self):
        return self._program
