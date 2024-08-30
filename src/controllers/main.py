# Name: Homeless Shelter Map Visualization
# Purpose: Visualizes various homeless shelters in the area of the City of Toronto through the form of a geographical map


# importing external libraries
import folium as fl
from folium.plugins import MiniMap
import pandas as pd
import pgeocode
import numpy as np

# importing project files
from src import constants as c
# from src.models import shelter_class as sc
# from src.models import shelter_program_class as spc
# from src.models import shelter_class_sector_program as ssc, shelter_class_weather_program as wsc
from src.models import shelter as sc
from src.models import shelter_program as spc
from src.models import shelter_class_weather_program as wsc
from src.models import womenShelter as ws
from src.models import menSector as ms
from src.models import youthSector as ys
from src.models import CoedSector as cs
from src.utils import data_utils
from src import constants as c


# declaring main function
def main():
    # initializing pandas dataframe display settings
    init_options()
    # initializing pandas dataframe which is used throughout project
    data = data_utils.init_data( c.DATA_FILE_NAME)

    # adding a new column based on an existing column - new column identifies if shelter is a weather shelter
    init_weather(data)

    # using pgeocode, a library which converts the postal code of a location into its geographic coordinates
    # initializing the country reference of postal code interpretation as Canada
    nominatim = pgeocode.Nominatim("ca")
    # using a pgeocode function to convert the postal code data into coordinate
    coordinates = data[c.DATA_POSTAL_CODE].apply(lambda x: nominatim.query_postal_code(x))
    # loading map visualization
    map = fl.Map(location=(43.6532, -79.3832), zoom_start=10, )
    MiniMap(toggle_display=True).add_to(map)

    coed_marker_cluster, men_marker_cluster, sector_marker_cluster, weather_marker_cluster, weather_shelter_marker_cluster, women_shelter_marker_cluster, youth_marker_cluster = init_layers(
        map)

    # filling in "Nan" values of coordinates with 0 to ensure that no errors occur
    clean_coordinates(coordinates)

    # transferring coordinate data into dataframe
    data[c.DATA_LATITUDE] = coordinates["latitude"]
    data[c.DATA_LONGITUDE] = coordinates["longitude"]
    # print(data)
    #
    # # #adding a new column based on an existing column - new column identifies if shelter is in the city of Toronto
    # # #if the city is Toronto, the value 'True' is returned, or else if it isn't, 'false' is returned
    # # #converts string to boolean
    # # data["IS_CITY_TORONTO"] = data["SHELTER_CITY"]
    # data["IS_CITY_TORONTO"] = np.where(data["IS_CITY_TORONTO"] == "Toronto", True, False)
    # #converting the date values of the dataset to a new type of date value which includes the month as a visible word
    # new_date = pd.to_datetime((data["OCCUPANCY_DATE"]))
    # data["OCCUPANCY_DATE"] = new_date.dt.strftime("%d %B %y")

    # initializes the shelter objects
    # creates lists to store the different shelter objects
    women_programs, men_prog, youth_program, coed_program, weather_shelter_list = init_shelters(data)
    # adding maps from different shelter lists to the corresponding clusters
    for x in weather_shelter_list:
        x.addToMap(weather_marker_cluster)
    for x in weather_shelter_list:
        x.addWeatherShelter( weather_shelter_marker_cluster)
        x.createicon(data)
    for i in women_programs:
        i.addWomenToDefaultMap( sector_marker_cluster)
        i.get_women_marker( women_shelter_marker_cluster)
    for k in men_prog:
        k.addMenToDefaultMap( sector_marker_cluster)
        k.get_men_marker( men_marker_cluster)
    for e in youth_program:
        e.addYouthToDefaultMap(sector_marker_cluster)
        e.get_youth_marker( youth_marker_cluster)
    for j in coed_program:
        j.addCoedToDefaultMap( sector_marker_cluster)
        j.get_coed_marker( coed_marker_cluster)
    # exporting the map
    map.save("index.html")


def init_shelters(data):
    '''

    :param data: dict
               The dataframe which contains the shelter data.
    :return: array of initialized shelter objects.
    '''
    # initializing empty lists
    shelter_list = []

    for index, row in data.iterrows():
        shelterObject = sc.Shelter(row[c.DATA_ADDRESS], row[c.DATA_ORGANIZATION_NAME],
                                                  row[c.DATA_SHELTER_NAME], row[c.DATA_CITY],
                                                  row[c.DATA_POSTAL_CODE],
                                                  row[c.DATA_LATITUDE],
                                                  row[c.DATA_LONGITUDE], data)

    shelter_program_list = []

    # creating objects in a loop by providing inputs to object parameters
    # adding objects to array
    for index, row in data.iterrows():
        shelterProgramObject = spc.shelterProgram(row[c.DATA_ADDRESS], row[c.DATA_ORGANIZATION_NAME],
                                                  row[c.DATA_SHELTER_NAME], row[c.DATA_CITY],
                                                  row[c.DATA_POSTAL_CODE],
                                                  row[c.DATA_LATITUDE],
                                                  row[c.DATA_LONGITUDE],
                                                  row[c.DATA_PROGRAM_NAME], data)
        shelter_program_list.append(shelterProgramObject)

    weather_shelter_list = []
    for index, row in data.iterrows():
        # loops through the different values in a row and assigns them to a new shelter object
        # new shelter objects are created until the looping of the dataset ends
        weatherShelterObject = wsc.WeatherShelter(row[c.DATA_ADDRESS], row[c.DATA_ORGANIZATION_NAME],
                                                  row[c.DATA_SHELTER_NAME], row[c.DATA_CITY],
                                                  row[c.DATA_POSTAL_CODE],
                                                  row[c.DATA_LATITUDE],
                                                  row[c.DATA_LONGITUDE],
                                                  row[c.DATA_WEATHER], row[c.DATA_PROGRAM_NAME], data)
        # adds the newly created shelter object to the list of stored shelters
        weather_shelter_list.append(weatherShelterObject)

    women_programs = []
    men_programs = []
    youth_programs = []
    coed_programs = []
    for index, row in data.iterrows():
        sectorShelterObject = ws.womenShelter(row[c.DATA_ADDRESS], row[c.DATA_ORGANIZATION_NAME],
                                              row[c.DATA_SHELTER_NAME], row[c.DATA_CITY],
                                              row[c.DATA_POSTAL_CODE],
                                              row[c.DATA_LATITUDE],
                                              row[c.DATA_LONGITUDE],
                                              row[c.DATA_SECTOR], row[c.DATA_PROGRAM_NAME], data)
        women_programs.append(sectorShelterObject)
    for index, row in data.iterrows():
        sectorShelterObject = ms.ProgramMen(row[c.DATA_ADDRESS], row[c.DATA_ORGANIZATION_NAME],
                                            row[c.DATA_SHELTER_NAME], row[c.DATA_CITY],
                                            row[c.DATA_POSTAL_CODE],
                                            row[c.DATA_LATITUDE],
                                            row[c.DATA_LONGITUDE],
                                            row[c.DATA_SECTOR], row[c.DATA_PROGRAM_NAME], data)
        men_programs.append(sectorShelterObject)
    for index, row in data.iterrows():
        sectorShelterObject = ys.youthShelter(row[c.DATA_ADDRESS], row[c.DATA_ORGANIZATION_NAME],
                                              row[c.DATA_SHELTER_NAME], row[c.DATA_CITY],
                                              row[c.DATA_POSTAL_CODE],
                                              row["Shelter_Coordinates_Latitude"],
                                              row["Shelter_Coordinates_Longitude"],
                                              row[c.DATA_SECTOR], row[c.DATA_PROGRAM_NAME], data)
        youth_programs.append(sectorShelterObject)

    for index, row in data.iterrows():
        sectorShelterObject = cs.CoedShelter(row[c.DATA_ADDRESS], row[c.DATA_ORGANIZATION_NAME],
                                             row[c.DATA_SHELTER_NAME], row[c.DATA_SECTOR],
                                             row[c.DATA_POSTAL_CODE],
                                             row["Shelter_Coordinates_Latitude"],
                                             row["Shelter_Coordinates_Longitude"],
                                             row[c.DATA_SECTOR], row[c.DATA_PROGRAM_NAME], data)

        coed_programs.append(sectorShelterObject)
    return women_programs, men_programs, youth_programs, coed_programs, weather_shelter_list


def clean_coordinates(coordinates):
    """

    :param coordinates:
    :return: none
    """
    # filling invalid coordinates with the value of 0
    coordinates["latitude"] = coordinates["latitude"].fillna(0)
    coordinates["longitude"] = coordinates["longitude"].fillna(0)


def init_weather(data):
    """

    :param data: dict
                The dataframe with all shelter information.
    :return: none
    """
    # Creating a new weather column based on if a program's name contains the word "Weather
    # if it contains the word "Weather", return true, else, return false
    # These shelters are used for purposes of weather emergencies
    data[c.DATA_WEATHER] = data[c.DATA_PROGRAM_NAME]
    data[c.DATA_WEATHER] = np.where(data[c.DATA_WEATHER].str.contains("Weather"), True, False)


def init_options():
    """
    Initializes dataframe display setting
    :return: none
    """
    pd.set_option('display.width', None)
    # Environment settings:
    pd.set_option('display.max_column', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_seq_items', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('expand_frame_repr', True)


def init_layers(map):
    """

    :param map: folium map object
    :return: folium marker clusters
    """
    # initializing feature groups
    # These groups are featured on the side menu under the dropdown in the UI
    fgWeatherMap = fl.FeatureGroup(name="Weather Shelters", show=True).add_to(map)
    fgSectorMap = fl.FeatureGroup(name="Shelter Sectors", show=True).add_to(map)
    fgWeatherShelterMap = fl.FeatureGroup(name="Weather Shelter Map", show=True).add_to(map)
    fgWomenShelterMap = fl.FeatureGroup(name="Women Shelter Map", show=True).add_to(map)
    fgMenShelterMap = fl.FeatureGroup(name="Men Shelter Map", show=True).add_to(map)
    fgYouthShelterMap = fl.FeatureGroup(name="Youth Shelter Map", show=True).add_to(map)
    fgCoedShelterMap = fl.FeatureGroup(name="Coed Shelter Map", show=True).add_to(map)

    # adding side menu to map UI
    fl.LayerControl().add_to(map)
    # adding marker clusters to feature groups
    # clusters act as a layer, storing all data which is added to it
    weather_marker_cluster = fl.plugins.MarkerCluster().add_to(fgWeatherMap)
    sector_marker_cluster = fl.plugins.MarkerCluster().add_to(fgSectorMap)
    weather_shelter_marker_cluster = fl.plugins.MarkerCluster().add_to(fgWeatherShelterMap)
    women_shelter_marker_cluster = fl.plugins.MarkerCluster().add_to(fgWomenShelterMap)
    men_marker_cluster = fl.plugins.MarkerCluster().add_to(fgMenShelterMap)
    youth_marker_cluster = fl.plugins.MarkerCluster().add_to(fgYouthShelterMap)
    coed_marker_cluster = fl.plugins.MarkerCluster().add_to(fgCoedShelterMap)

    return coed_marker_cluster, men_marker_cluster, sector_marker_cluster, weather_marker_cluster, weather_shelter_marker_cluster, women_shelter_marker_cluster, youth_marker_cluster


# calling main function
if __name__ == "__main__":
    main()
