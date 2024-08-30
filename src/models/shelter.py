
import folium as fl
from src import constants as c


# declaring shelter class
class Shelter:
    """
    A shelter object that holds information regarding its background information, such as its location, sector of people
    which it serves, information regarding the organization it belongs to, as well changing data regarding
    its occupancy. It can also calculate different types of averages with its occupancy data, including annual
    average occupancy, and annual average rate of occupancy.

    Attributes
    ----------
    address : str
            The address of the shelter
    organizationName : str
            The name of the organization that runs the shelter - this is different from the name of the shelter
    name : str
            The name of the shelter

    city : str
            The name of the city in which the shelter resides
    postalCode : str
            The postal code of the shelter (different from address)
    latitude : float
            The latitude of the shelter
    longitude: float
            The longitude of the shelter
    data: dict
            The dataframe which contains the shelter data.

    Methods
    -------
    calculateAveragedDailyOccupancy() -> int
                    The daily average of the number of people who occupy a given shelter every day throughout 2020
    calculateAverageDailyOccupancyRate() -> float
                    The daily average of the percentage of occupancy of a given shelter over the year
    popUpText() -> str
                    Creates a message including the shelter's information such as name, city, etc.
    addMap() -> void
                    Adds/displays the icon of the shelter to the map

    getAddress() -> str
                    Returns the address of the shelter
    getOrganizationName() -> str
                    Returns the name of the shelter's organization
    getShelterName() -> str
                    Returns the name of the shelter
    getCity() -> str
                    Returns the name of the city that the shelter is in
    getPostalCode() -> str
                    Returns the postal code of the shelter
    getLongitude() -> float
                    Returns the longitude of the shelter
    getLatitude() -> float
                    Returns the latitude of the shelter
    getData() -> dict
                    Returns the pandas dataframe containing the shelter the data.


     """

    # initializing constructor
    def __init__(self, address, organizationName, name, city, postalCode, latitude, longitude, data):
        """
        Constructor to build a shelter object

        Parameters
        ----------
        organization_name: str
               The name of the organization which owns the shelter
        name: str
               The name of the shelter
        address: str
               The adress of the shelter
        city: str
              The city which the shelter is located in
        postalCode: str
              The postal code of the shelter
        latitude:  float
              The latitude of the shelter
        longitude: float
              The longitude of the shelter
        data: dict
              Shelter data

        """

        self._address = address
        self._organization = organizationName
        self._name = name
        self._city = city
        self._postalCode = postalCode
        self._latitude = latitude
        self._longitude = longitude
        self._data = data

    def calculateAverageDailyOccupancy(self):
        '''
        Calculates average daily occupancy of a shelter over the year

        Returns
        ------ -
        int
            The average daily occupancy of a shelter over the year

        '''

        # variables to store the running average occupancy sum and the running number of shleters
        average_occ_sum = 0
        number_of_shelters = 0
        # iterating through the rows of the dataframe and checking if a program is in the same shelter location as the
        # program attribute of the current object

        for row in self.getData().iterrows():
            if row[c.DATA_POSTAL_CODE] == self._postalCode:
                # adding the occupancies of all days in the year for a given program and dividing by number of days to find average occupancy
                # for one program
                occu_sum = sum(row[c.DATA_OCCUPANCIES])
                # adding each average to average_occ_sum
                average_occ_sum += occu_sum / len(row[c.DATA_OCCUPANCIES])
                number_of_shelters += 1
        # dividing by total number of programs to find average across all programs for one shelter
        average_occ_sum /= number_of_shelters
        average_occ_sum = average_occ_sum * 100
        return average_occ_sum

    def calculateAverageDailyOccupancyRate(self):
        '''
        Calculates the average daily percentage of occupancy of a shelter over the year

        Returns
        -------
        float
            The value of the average daily rate of occupancy for the shelter
        '''
        # same process as calculateAverageDailyOccupancy except now we take average of each occupancy divided by
        # capacity to calculate rate of occupancy
        occupancies_rate_sum = 0
        numShelters_ = 0
        for row in self.getData().iterrows():
            if row[c.DATA_POSTAL_CODE] == self._postalCode:
                occ_rate = 0
                # iterating over list to use index to divide each occupancy on a day by its capacity
                for index in row[c.DATA_OCCUPANCIES]:
                    if row[c.DATA_CAPACITIES][index] != 0:
                        occ_rate += row[c.DATA_OCCUPANCIES][index] / row[c.DATA_CAPACITIES][index]
                        occupancies_rate_sum += occ_rate
            numShelters_ += 1
        # multiplying by 100 to get in percent form
        occupancies_rate_sum = (occupancies_rate_sum / numShelters_) * 100
        return occupancies_rate_sum

    def popUpText(self):
        """
        :return: popUpText: The text which will displayed on the shelter icon popup.

        """
        # generating text that will be displayed on popup with shelter's information
        popUpText = (f"Organization Name: {self.getOrganizationName()}, Shelter Address: {self.getAddress()}, "
                     f"Name of Shelter: {self.getShelterName()}, City: {self.getCity()}, Postal Code: {self.getPostalCode()}, "
                     f" Average Annual Occupancy:{self.calculateAverageDailyOccupancy()}, Average Annual Rate of Occupancy:"
                     f"{self.calculateAverageDailyOccupancyRate()}% ")
        return popUpText

    def addToMap(self, map_cluster):
        """

        :param map_cluster: the map cluster to which the map icons will be added.
        :return: none
        """
        # creating a folium marker which is added to map cluster
        fl.Marker(
            location=(self.getLatitude(), self.getLongitude()),
            popup=self.popUpText(),
            axis=1
        ).add_to(map_cluster)

    # public getter functions for private attributes of the class

    def getAddress(self):
        return self._address

    def getOrganizationName(self):
        return self._organization

    def getShelterName(self):
        return self._name

    def getCity(self):
        return self._city

    def getPostalCode(self):
        return self._postalCode

    def getLongitude(self):
        return self._longitude

    def getLatitude(self):
        return self._latitude

    def getData(self):
        return self._data
