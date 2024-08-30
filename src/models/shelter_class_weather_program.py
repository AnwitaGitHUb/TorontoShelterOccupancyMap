
import numpy as np
from src import constants as c
from src.models import shelter_program as spc
import folium as fl



class WeatherShelter(spc.shelterProgram):
    def __init__(self, address, organizationName, name, city, postalCode, latitude,
                 longitude, weather, programName, data):
        # inheriting attributes from "shelterProgram"
        super().__init__(address, organizationName, name, city, postalCode, latitude,
                         longitude, programName, data)
        # adding "weather" attribute of type "bool"
        self._weather = weather

    # function to display on map with following characteristics:
    # if shelter program is a weather program, icon is blue and symbol is "cloud"
    # if shelter program is not a weather program, icon is "red" and symbol is "person-shelter"
    def addToMap(self, type_of_map):
        """

        :param type_of_map: marker cluster to which this map should be added
        :return: none
        """
        if self.getWeather():
            fl.Marker(
                location=(self.getLatitude(), self.getLongitude()),
                axis=1,
                popup=self.popUpText(),
                icon=fl.Icon(prefix="fa", color="blue", icon="cloud")
            ).add_to(type_of_map)
        else:
            if not self.getWeather():
                fl.Marker(
                    location=(self.getLatitude(), self.getLongitude()),
                    axis=1,
                    popup=self.popUpText(),
                    icon=fl.Icon(prefix="fa", color="red", icon="person-shelter")
                ).add_to(type_of_map)

    # function to display on map just if shelter program of object is a weather program
    # this function is also meant to use a different marker cluster than above function
    def addWeatherShelter(self, type_of_map):
        """

        :param type_of_map: marker cluster to which this map should be added
        :return: none
        """
        if self.getWeather():
            fl.Marker(
                location=(self.getLatitude(), self.getLongitude()),
                axis=1,
                popup=self.popUpText(),
                icon=self.createicon(self.getData())
            ).add_to(type_of_map)

    # creating a sorted list of occupancies for weather programs
    def sortedOccupancyData(self, getData):
        """

        :param getData: pandas dataframe that stores shelter information
        :return: average_occupancies: a list of sorted weather program occupancies
        """
        # creating new dataset by filtering original dataset to just have rows that have weather programs
        quartile = getData[getData[c.DATA_WEATHER] == True]
        #  initializing a list to store occupancies
        average_occupancies = []
        for index, row in quartile.iterrows():
            if len(row[c.DATA_OCCUPANCIES]) != 0:
                # calculating average
                average_occupancy = (sum(row[c.DATA_OCCUPANCIES]) / len(row[c.DATA_OCCUPANCIES]))
                # adding average to list
                average_occupancies.append(average_occupancy)
        # sorting use sort function
        average_occupancies.sort()
        return average_occupancies

    # calculating different quartiles of sorted data
    def firstQuartile(self):
        """
        :return: firstQuartile: a float which represents the first quartile value of the sorted average occupancies
        """
        if self.getWeather():
            # use numpy to calculate quartile
            firstQuartile = np.quantile(self.sortedOccupancyData(self.getData()), 0.25)
            return firstQuartile

    def secondQuartile(self):
        """

        :return: secondQuartile: a float which represents the second quartile value of the sorted average occupancies
        """
        if self.getWeather():
            secondQuartile = np.quantile(self.sortedOccupancyData(self.getData()), 0.50)
            return secondQuartile

    def thirdQuartile(self):
        """

        :return: thirdQuartile: a float which represents the third quartile value of the sorted average occupancies
        """
        if self.getWeather():
            thirdQuartile = np.quantile(self.sortedOccupancyData(self.getData()), 0.75)
            return thirdQuartile

# based on where a weather object's occupancy falls between the quartiles, the object's icon will have a certain color
    def createicon(self, getData):
        """

        :param getData: pandas dataframe that contains shelter information
        :return: icon: folium icon to display on map
        """
        # checking to see if object is a weather program
        if self.getWeather():
            # if occupancy is between/ equal to 3rd and 4th quartile, make the icon red
            if self.calculateAverageDailyOccupancy() >= self.thirdQuartile():
                icon = fl.Icon(prefix="fa", color="red", icon="cloud")
                return icon
            # if occupancy is between/ equal to 2nd and 3rd quartile, make the icon orange
            elif self.calculateAverageDailyOccupancy() > self.secondQuartile(
                    ) and self.calculateAverageDailyOccupancy() <= self.thirdQuartile():
                icon = fl.Icon(prefix="fa", color="orange", icon="cloud")
                return icon
            # if the occupancy is between/ equal to 1st and 2nd quartile, make icon beige
            elif self.calculateAverageDailyOccupancy() > self.firstQuartile(
                    ) and self.calculateAverageDailyOccupancy() <= self.secondQuartile():
                icon = fl.Icon(prefix="fa", color="beige", icon="cloud")
                return icon
            # if the occupancy is under the 1st quartile, make the icon green
            else:
                icon = fl.Icon(prefix="fa", color="green", icon="cloud")
                return icon

    # getting weather attribute
    def getWeather(self):
        return self._weather
